# from app.utils.pdf_downloader import download_pdf_text
from app.AI.generateBlog.utils.pdf_downloader import download_pdf_text
from app.AI.generateBlog.utils.beauty_output import format_jurnal_list, tavily_format_result, gnews_format_result, format_blog_body
from app.AI.generateBlog.utils.summarize import summarize_with_gemini, summarize_blog
from app.AI.generateBlog.service.blogService import postToN8n
from app.AI.generateBlog.prompts import AllAgentPrompts
from app.AI.generateBlog.models import AgentState, toolStructuredOutput, NextStepStructuredOutput, HeaderStructuredOutput, BodyStructuredOutput, FooterStructuredOutput, RevisionStructuredOutput, SentimentStructuredOutput,RevisionByHumanStructuredOutput, DetailBlogStructuredOutput
from app.AI.generateBlog.tools import SearchTools
from langchain_core.messages.base import BaseMessage
from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt, Command
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_openai import ChatOpenAI
from typing import Dict, Any, List, Sequence
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
from dotenv import load_dotenv
from langchain_core.tools import Tool, tool, StructuredTool
from langgraph.prebuilt import ToolNode
from IPython.display import display,Image
# from contextlib import contextmanager
# import networkx as nx
# import matplotlib.pyplot as plt
load_dotenv()


class Workflow:
    def __init__(self, checkpointer):
        self.llm_for_reasoning = ChatOpenAI(model="gpt-4o", temperature=0.7)
        self.llm_for_explanation = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
        self.prompts = AllAgentPrompts()
        self.tools = SearchTools()
        self.checkpointer = checkpointer
        self.workflow = self._build_workflow()

    def _build_workflow(self):
        graph = StateGraph(AgentState)
        graph.add_node("search_tools", ToolNode([
            Tool.from_function(
                func=self.tavily_search,
                name="tavily_search",
                description="""
                Gunakan tool ini untuk mencari informasi umum atau fakta yang relevan dengan topic.
                
                params:
                - keyword: Kata kunci
                """
            ),Tool.from_function(
                func=self.wikipedia_search,
                name="wikipedia_search",
                description="""
                Gunakan tool ini untuk mencari informasi biografis tentang individu, sejarah konsep atau istilah, atau definisi mendalam.

                params:
                - keyword: Kata kunci
                """
            ),Tool.from_function(
                func=self.arxiv_search,
                name="arxiv_search",
                description="""
                Gunakan tool ini untuk mencari paper ilmiah dan sumber teknis kredibel.

                params:
                - keyword: Kata kunci
                """
            ),StructuredTool.from_function(
                func=self.serper_search,
                name="serper_search",
                description="""
                Gunakan tool ini untuk informasi dari jurnal ilmiah, artikel penelitian mendalam, atau sumber-sumber teknis yang kredibel, terutama jika topik memerlukan landasan ilmiah atau data spesifik.

                params:
                - keyword: Kata kunci untuk mencari jurnal yang relevan
                - topic: Rangkuman/topic dari blog yang sedang kamu buat.
                """
            ),Tool.from_function(
                func=self.unsplash,
                name="unsplash",
                description="""
                Gunakan tool ini untuk mencari gambar thumbnail di unsplash yang sesuai dengan blog tersebut.
                """
            )]
        ))

        graph.add_node("generate_prompt", self._generate_prompt)
        graph.add_node("gathering_information", self._gathering_information)
        graph.add_node("save_tool_message", self._save_tool_messages)
        graph.add_node("decision", self._decision_next_step)
        graph.add_node("plus_retry", self._plus_retry)
        graph.add_node("generate_header", self._generate_header)
        graph.add_node("generate_body", self._generate_body)
        graph.add_node("generate_footer", self._generate_footer)
        graph.add_node("agent_validation", self._agent_validation)
        graph.add_node("ask_human", self._ask_human)
        graph.add_node("human_in_the_loop", self._human_in_the_loop)
        graph.add_node("sentiment_analysis", self._sentiment_analysis)
        graph.add_node("revision_by_human", self._agent_revision_by_human)
        graph.add_node("changing_blog", self._changing_blog_content)
        graph.add_node("complete_node", self._complete_node)
        graph.add_node("generate_detail_blog", self._generate_detail_blog)

        graph.add_edge(START, "generate_prompt")
        graph.add_edge("gathering_information", "search_tools")
        graph.add_edge("search_tools","save_tool_message")
        graph.add_edge("generate_prompt", "gathering_information")
        graph.add_edge("gathering_information","search_tools")
        graph.add_edge("search_tools","save_tool_message")
        graph.add_edge("save_tool_message","decision")

        graph.add_conditional_edges(
            "decision",
            self._next_step_router,
            {
                "search_again":"plus_retry",
                "next_step":"generate_header"
            }
        )

        graph.add_conditional_edges(
            "plus_retry",
            self._retry_router,
            {
                "stop":"generate_header",
                "next":"gathering_information"
            }
        )
        
        graph.add_edge("generate_header", "generate_body")
        graph.add_edge("generate_body", "generate_footer")
        graph.add_edge("generate_footer", "agent_validation")
        graph.add_conditional_edges(
            "agent_validation",
            self._validation_router,
            {
                "next":"ask_human",
                "revision":"plus_retry"
            }
        )
        graph.add_edge("ask_human", "human_in_the_loop")
        graph.add_conditional_edges(
            "human_in_the_loop",
            self._ask_human_router,
            {
                "next":"sentiment_analysis",
                "complete":"complete_node"
            }
        )

        graph.add_edge("complete_node", END)
        graph.add_conditional_edges(
            "sentiment_analysis",
            self._sentiment_analysis_router,
            {
                "save":"generate_detail_blog",
                "revision":"revision_by_human"
            }
        )

        graph.add_edge("revision_by_human","changing_blog")
        graph.add_edge("changing_blog", "ask_human")
        graph.add_edge("generate_detail_blog", "complete_node")
        return graph.compile(checkpointer=self.checkpointer)


    def _generate_prompt(self, state:AgentState)-> Dict[str, Any]:
        topic = state.topic
        messages = self.prompts.agent_generate_prompt(topic)
        response = self.llm_for_reasoning.invoke(messages)
        print(f"Prompt: {response}")
        return {
            "messages": [HumanMessage(content=f"Tolong buatkan blog dengan topic: {state.topic}")],
            "prompt":response.content
        }

    
    def tavily_search(self,keyword:str) -> str:
        """
        Gunakan tool ini untuk mencari informasi umum atau fakta yang relevan dengan topic.
        
        params:
        - keyword: Kata kunci
        """
        result = self.tools.tavily_search(keyword)
        formated_result = tavily_format_result(result)
        print(f"LLM memanggil tool tavily: {formated_result}")
        return formated_result
    
    def wikipedia_search(self, keyword:str) -> str:
        """
        Gunakan tool ini untuk mencari informasi biografis tentang individu, sejarah konsep atau istilah, atau definisi mendalam.

        params:
         - keyword: Kata kunci
        """
        result = self.tools.wikipedia_search(keyword)
        print(f"LLM memanggil tool wikipedia: {result}")
        return result
    
    def arxiv_search(self, keyword:str) -> str:
        """
        Gunakan tool ini untuk mencari paper ilmiah dan sumber teknis kredibel.
        """
        result = self.tools.search_arxiv(keyword)
        print(f"LLM memanggil tool arxiv search: {result}")
        return result

    def unsplash(self, keyword:str) -> str: 
        """
        Gunakan tool ini untuk mencari gambar thumbnail di unsplash yang sesuai dengan blog tersebut.
        """
        thumbnail = self.tools.unsplash_picture(keyword)
        print(f"Tool unsplash: {thumbnail}")
        return thumbnail
    
    def serper_search(self, keyword:str, topic:str) -> str:
        """
        Gunakan tool ini untuk informasi dari jurnal ilmiah, artikel penelitian mendalam, atau sumber-sumber teknis yang kredibel, terutama jika topik memerlukan landasan ilmiah atau data spesifik.

        params:
         - keyword: Kata kunci untuk mencari jurnal yang relevan
         - topic: Rangkuman/topic dari blog yang sedang kamu buat.
        """
        result = self.tools.serper_search(keyword)
        system_message = [SystemMessage(content=f"""
        Kamu adalah penulis jurnal ilmiah profesional.
        Tugas kamu adalah memilih salah satu dari keempat hasil pencarian jurnal ilmiah.
        berikut adalah hasil pencariannya:
        {format_jurnal_list(result)}

        Pilih salah satu dari keempat jurnal tersebut yang menurutmu paling cocok dengan topic berikut:
        {topic}
        """),
        HumanMessage(content=f"""
        Tolong pilih salah satu jurnal yang paling cocok dengan topic berikut:
         {topic}

        berikut pilihan jurnalnya:
        {format_jurnal_list(result)}
""")]
        llm = self.llm_for_reasoning.with_structured_output(toolStructuredOutput)
        response = llm.invoke(system_message)
        pdf_url = response.pdfUrl
        download_result = download_pdf_text(pdf_url)
        print(f"LLM memanggil tool serper: {download_result}")
        return download_result
        
    def _gathering_information(self, state:AgentState):
        messages = state.messages
        tool_messages = [
            state.tavily_message,
            state.wiki_message,
            state.gNews_message,
            state.serper_message,
        ]
        prompt_template = self.prompts.searching_information(state.prompt,tool_messages[0], tool_messages[1], tool_messages[2], tool_messages[3],state.search_recomendation,state.retry)

        setup_llm = self.llm_for_reasoning.bind_tools([self.tavily_search, self.wikipedia_search, self.arxiv_search, self.serper_search, self.unsplash])
        response = setup_llm.invoke(prompt_template)

        return{
            "messages": [response]
        }

    def _save_tool_messages(self,state:AgentState) -> Dict[str, Any]:
        messages = state.messages
        result = {
            "tavily_message":"",
            "serper_message": "",
            "gNews_message":"",
            "wiki_message":"",
            "thumbnail":""
        }

        for item in messages:
            if isinstance(item, ToolMessage):
                if item.name == "tavily_search":
                    result["tavily_message"] = state.tavily_message + item.content
                elif item.name == "serper_search":
                    result["serper_message"] = state.serper_message + summarize_with_gemini(item.content) or item.content 
                elif item.name == "arxiv_search":
                    result["gnews_message"] = state.gNews_message + item.content
                elif item.name == "wikipedia_search":
                    result["wiki_message"] = state.wiki_message + item.content
                elif item.name == "unsplash":
                    result["thumbnail"] = item.content
        return result
    
    def _decision_next_step(self, state:AgentState) -> Dict[str, Any]:
        messages: Sequence[BaseMessage] = state.messages
        setup_llm = self.llm_for_reasoning.with_structured_output(NextStepStructuredOutput)
        prompt = self.prompts.agent_next_step_rekomendation(state.prompt,state.tavily_message,state.wiki_message,state.gNews_message,state.serper_message)
        response = setup_llm.invoke(messages + prompt)
        print(f"Alasan dari agent: {response.reason}")
        return {
            "search_again":response.search_again,
            "search_recomendation":response.recomendation
        }

    def _next_step_router(self, state:AgentState):
        search_again = state.search_again
        if search_again:  
            return "search_again"
        return "next_step"
    
    def _plus_retry(self,state:AgentState):
        retry = state.retry
        print(f"retry: {retry}")
        return {
            "retry": retry + 1
        }
    
    def _retry_router(self, state:AgentState):
        retry = state.retry
        if retry > 3:
            return "stop"
        return "next"
    
    def _generate_header(self,state:AgentState)-> Dict[str, Any]:
        setup_llm = self.llm_for_explanation.with_structured_output(HeaderStructuredOutput)
        prompt = self.prompts.agent_generate_header(state.prompt, state.tavily_message, state.wiki_message,state.gNews_message, state.serper_message)
        response = setup_llm.invoke(prompt)
        print(f"header: {response}")
        return {
            "header_result": response
        }
    
    def _generate_body(self, state:AgentState) -> Dict[str, Any]:
        setup_llm = self.llm_for_reasoning.with_structured_output(BodyStructuredOutput)
        prompt = self.prompts.agent_generate_body(state.prompt, state.tavily_message, state.wiki_message, state.gNews_message, state.serper_message, state.header_result)
        response = setup_llm.invoke(prompt)
        print(f"body: {response}")
        return {
            "body_result":response.body_result
        }
    
    def _generate_footer(self, state:AgentState) -> Dict[str, Any]:
        setup_llm = self.llm_for_reasoning.with_structured_output(FooterStructuredOutput)
        prompt = self.prompts.agent_generate_footer(state.header_result, format_blog_body(state.body_result))
        response = setup_llm.invoke(prompt)
        print(f"footer: {response}")
        return {
            "footer_result": response
        }
    
    def _agent_validation(self,state:AgentState) -> Dict[str, Any]:
        setup_llm = self.llm_for_reasoning.with_structured_output(RevisionStructuredOutput)
        prompt = self.prompts.agent_validation(state.prompt, state.header_result, format_blog_body(state.body_result), state.footer_result.conclusion)
        response = setup_llm.invoke(prompt)

        print(f"Agent vidation: {response}")
        return {
            "isValid": response.valid,
            "mistake": response.mistake,
            "revision_suggestion": response.repaired
        }
    
    def _validation_router(self, state:AgentState):
        if state.isValid:
            return "next"
        return "revision"
    
    def _initial(self, state:AgentState):
        print("========Initial NODE=======")
    def _ask_human(self, state:AgentState):
        header = state.header_result
        body = state.body_result
        footer = state.footer_result
        postToN8n(header.model_dump(),summarize_blog(format_blog_body(body)),footer.conclusion)
        print("====PostN8n====")
        
    def _human_in_the_loop(self, state:AgentState):
        human = interrupt("confirm")
        print(f"Human: {human}")
        return {
            "human_revision":human,
            "messages": state.messages + [HumanMessage(content=human)]
        }
    def _ask_human_router(self, state:AgentState):

        if state.human_revision:
            return "next"
        return "complete"
    
    def _sentiment_analysis(self, state:AgentState):
        setup_llm = self.llm_for_explanation.with_structured_output(SentimentStructuredOutput)
        prompt = self.prompts.sentiment_analysis(state.human_revision)
        response = setup_llm.invoke(prompt)
        print(f"sentimen analysis: {response}")
        return {
            "isValid":response.isAgree
        }

    def _sentiment_analysis_router(self, state:AgentState):
        if state.isValid:
            return "save"
        return "revision"
    
    def _agent_revision_by_human(self, state:AgentState)-> Dict[str, Any]:
        setup_llm = self.llm_for_reasoning.with_structured_output(RevisionByHumanStructuredOutput)
        prompt = self.prompts.revision_by_human(state.human_revision, state.header_result, format_blog_body(state.body_result), state.footer_result)
        response = setup_llm.invoke(prompt)
        print(f"revision by human: {response}")
        return {
            "mistake": response.mistake,
            "revision_suggestion": response.repaired,
            "section_blog": response.section_blog
        }
    
    def _changing_blog_content(self, state:AgentState):
        section = state.section_blog
        if section == 'header':
            return {
                "header_result": state.revision_suggestion
            }
        elif section == 'body':
            return {
                "body_result": state.revision_suggestion
            }
        return {
            "footer_result": state.revision_suggestion
        }

    def _complete_node(self, state:AgentState):
        print(f"state: {state.human_revision}")
        print("=====END======")
    
    def _generate_detail_blog(self, state:AgentState) -> Dict[str, Any]:
        setup_llm = self.llm_for_explanation.with_structured_output(DetailBlogStructuredOutput)
        prompt = self.prompts.generate_detail_blog(state.header_result, format_blog_body(state.body_result), state.footer_result)
        response = setup_llm.invoke(prompt)
        print(f"Detail blog: {response}")
        return {
            "detail_blog": response
        }

        
    def continue_execution(self, message:str):
        config = {"configurable": {"thread_id": "thread_123"}}
        return self.workflow.invoke(Command(resume=message), config=config)

    def run(self, topic:str):
        state = {
            "messages": [],
            "topic":topic,
            "prompt":"",
            "tavily_message":"",
            "serper_message": "",
            "gNews_message": "",
            "wiki_message": "",
            "thumbnail":"",
            "search_again":False,
            "search_recomendation":"",
            "header_result": "",
            "body_result": "",
            "footer_result": "",
            "detail_blog": "",
            "isValid": False,
            "human_revision":"",
            "mistake": "",
            "section_blog":"",
            "revision_suggestion": None,
            "retry": 0
        }
        # for event in workflow.stream(state):
        #     for key, val in event.items():
        #         print(f"🧠 Node: {key}")
        #         for msg in val["messages"]:
        #             if isinstance(msg, AIMessage):
        #                 print(f"\n🤖 AI: {msg.content}")
        #                 if msg.tool_calls:
        #                     for tc in msg.tool_calls:
        #                         print(f"🔧 Memanggil tool: {tc['name']} dengan argumen {tc['args']}")
        #             elif isinstance(msg, ToolMessage):
        #                 print(f"\n🛠️ Hasil Tool ({msg.tool_call_id}): {msg.content}")
        #             elif isinstance(msg, HumanMessage):
        #                 print(f"\n🙋 Human: {msg.content}")
        #         print("=" * 60)
        config = {"configurable": {"thread_id": "thread_123"}}
        return self.workflow.invoke(state, config=config)

    def visualize_workflow(self):
        graph = self.workflow.get_graph()
        print("[visualize_workflow] Mencoba memvisualisasikan graph...")

        try:
            img_bytes = graph.draw_png()  # Mengembalikan image dalam bentuk bytes
            display(Image(data=img_bytes))
        except Exception as e:
            print("[visualize_workflow] Gagal menggambar graph:", str(e))
            try:
                print("[visualize_workflow] Coba tampilkan dengan ASCII:")
                graph.print_ascii()
            except Exception as e2:
                print("[visualize_workflow] Gagal menampilkan ASCII:", str(e2))

# if __name__ == "__main__":
#     wf = Workflow()
#     result = wf.run("Sistem informasi di era AI")
#     wf.continue_execution("Udah okeh")

    # print(result)
    # print(wf.serper_search("Sistem informasi di era AI", "Mengungkap Peran Sistem Informasi di Era AI: Transformasi Digital yang Tak Terelakkan"))

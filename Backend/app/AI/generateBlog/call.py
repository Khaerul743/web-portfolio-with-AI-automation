from contextlib import ExitStack
from langgraph.checkpoint.sqlite import SqliteSaver
from app.AI.generateBlog.workflow import Workflow
# from workflow import Workflow

def execute_workflow(message, node):
    with ExitStack() as stack:
        # Gunakan file SQLite untuk persistent state
        checkpointer_cm = SqliteSaver.from_conn_string("app/AI/generateBlog/database/state_memory.sqlite")
        checkpointer = stack.enter_context(checkpointer_cm)

        # Buat instance Workflow
        wf = Workflow(checkpointer)

        # Jalankan workflow
        # wf.visualize_workflow()
        if node == "start":
            return wf.run(message)
        else:
            return wf.continue_execution(message)

# if __name__ == "__main__":
#     print(execute_workflow("oke udah bagus", "next"))
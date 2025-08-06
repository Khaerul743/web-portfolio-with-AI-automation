import os
import dotenv
from flask import request, jsonify
from app.utils.response import response
from app.utils.authHeader import authHeader
from app.AI.generateBlog.call import execute_workflow
from app.models.blog import Blog
from app.models.tag import Tag
from app.models.body import Body
from app.models.content import Content
from app.models.introduction import Introduction
from app.AI.generateBlog.models import HeaderStructuredOutput, DetailBlogStructuredOutput, FooterStructuredOutput, BodyResultFormat
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from app import db
from app.AI.RAG.agent import agent

def run_agent():
    agent_key = request.headers.get("agent-key")
    api_key = os.getenv("API_KEY")
    
    if agent_key != api_key or not agent_key:
        return response("Invalid api key.",[],403)

    payload = request.json
    message = payload.get("message")

    if not message:
        return response("Message is required", [], 400)
    
    try:
        result = agent.run(message)
        return jsonify({"message":message, "response":result})
    
    except Exception as e:
        return response(e,[],500)

def generateBlog():
    auth = authHeader()
    if auth:
        return response("Invalid api key.", [], 403)
    try:
        payload = request.json
        topic = payload.get("topic")
        print(payload)

        if not topic:
            return response("Topic field is required.",[],400)

        result = execute_workflow(topic, "start")

        return response("Berhail", [], 200)
    except Exception as e:
        print(f"Gagal membuat struktur blog: {str(e)}")
        return response("Gagal membuat struktur blog", [], 500)


def humanResponse():
    auth = authHeader()
    if auth:
        return response("Invalid api key.", [], 403)
    try:
        payload = request.json
        print(payload)
        # return response("Berhail", [], 200)
        message = payload.get("message")

        if not message:
            return response("field field is required.",[],400)

        result = execute_workflow(message, "next")
        title = result["detail_blog"].title
        headline = result["detail_blog"].headline
        author = result["detail_blog"].author
        tags = result["detail_blog"].tags
        thumbnail = result["thumbnail"]
        description= result["detail_blog"].description
        read_time= result["detail_blog"].readTime
        # tags = payload.get("tags", [])

        if not title or not description:
            return response("Semua field harus diisi.",[],400)

        blog = Blog(
            title=title,
            headline=headline,
            author=author,
            description=description,
            thumbnail=thumbnail,
            read_time=read_time
        )

        for tag_id in tags:
            tag = Tag.query.get(tag_id)
            if tag:
                blog.tags.append(tag)
        
        db.session.add(blog)
        db.session.flush()

        header_blog = Introduction(blog_id=blog.id, hook=result["header_result"].hook, purpose=result["header_result"].purpose)
        db.session.add(header_blog)

        body_blog = Body(blog_id=blog.id, conclusion=result["footer_result"].conclusion)
        db.session.add(body_blog)
        db.session.flush()

        content_blog = [
            Content(body_id = body_blog.id, subtitle=section.subtitle, content = section.content) 
            for section in result["body_result"]
        ]

        db.session.add_all(content_blog)
        db.session.commit()
        return response("Berhail membuat blog", {"hook":header_blog.hook, "purpose":header_blog.purpose}, 200)
    except Exception as e:
        print(f"Gagal membuat blog: {str(e)}")
        return response("Gagal membuat blog", [], 500)

    
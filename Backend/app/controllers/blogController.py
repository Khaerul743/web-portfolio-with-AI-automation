import os
from app.utils.response import response
from app.utils.authHeader import authHeader
from app.models.blog import Blog
from app.models.tag import Tag
from app.models.introduction import Introduction
from app.models.content import Content
from app.models.body import Body
from flask import request
from app import db
from dotenv import load_dotenv
load_dotenv()

def getAllBlogDisplay():
    auth = authHeader()
    if auth:
        return response("Invalid api key.", [], 403)
    try:
        data = Blog.query.filter_by(accepted=True).all()

        return response("berhasil", [blog.to_dict() for blog in data],200)
    except Exception as e:
        print(f"Terjadi kesalahan saat mengambil data: {e}")
        return response(f"Terjadi kesalah saat mengambil data",[],500)

def getBlogById(blog_id):
    auth = authHeader()
    if auth:
        return response("Invalid api key.", [], 403)
    try:
        get_blog = Blog.query.get(blog_id)
        blog = get_blog.to_dict()
        if not blog:
            return response("Blog tidak ditemukan", [], 404)
        get_header = Introduction.query.filter_by(blog_id=blog_id).first()
        header = get_header.to_dict()

        get_footer = Body.query.filter_by(blog_id=blog_id).first()
        footer = get_footer.to_dict()
        body_id = footer["id"]

        get_content = Content.query.filter_by(body_id = body_id).all()
        content = [item.to_dict() for item in get_content]

        blog["introduction"] = header
        blog["body"] = content
        blog["conclusion"] = footer["conclusion"]
        del blog["description"]
        del blog["thumbnail"]

        return response("Berhasil mengambil blog by id",blog, 200)
    
    except Exception as e:
        print(f"Terjadi kesalahan saat mengambil data: {e}")
        return response(f"Terjadi kesalah saat mengambil data",[],500)       

def addBlog():
    auth = authHeader()
    if auth:
        return response("Invalid api key.", [], 403)
    try:
        payload = request.json

        title = payload.get("title")
        description= payload.get("description")
        thumbnail= payload.get("thumbnail")
        read_time= payload.get("read_time", 0)
        tags = payload.get("tags", [])

        if not title or not description or not thumbnail:
            return response("Semua field harus diisi.",[],400)

        blog = Blog(
            title=title,
            description=description,
            thumbnail=thumbnail,
            read_time=read_time
        )

        for tag_id in tags:
            tag = Tag.query.get(tag_id)
            if tag:
                blog.tags.append(tag)

        db.session.add(blog)
        db.session.commit()

        return response("Berhasil menambahkan data baru.", blog.to_dict(), 201)
    except Exception as e:
        db.session.rollback()
        print(f"Terjadi kesalahan saat menambahkan data: {e}")
        return response(f"Terjadi kesalah saat menambahkan data",[],500) 

    
# def updateBlog(blog_id):
#     authHeader(response=response)

#     try:
#         if not blog_id:
#             return response("blog id is required", [], 400)
        
#         data = mongo.db.blogs.find_one({"blog_id":blog_id})

#         if not data:
#             return response("Blog is not defined", [], 404)
#         payload = request.json

#         title = payload.get("title", data["title"])
#         description= payload.get("description", data["description"])
#         content = payload.get("content", data["content"])
#         thumbnail= payload.get("thumbnail", data["thumbnail"])
#         date= payload.get("date", data["date"])
#         readTime= payload.get("readTime", data["readTime"])
#         category=  payload.get("category", data["category"])

        
#         mongo.db.blogs.update_one(
#             {"blog_id":blog_id},
#             {"$set":{
#                 "title":title,
#                 "description":description,
#                 "content": content,
#                 "thumbnail":thumbnail,
#                 "date":date,
#                 "readTime":readTime,
#                 "category":category
#             }}
#         )

#         return response(
#             "Data berhasil diperbarui.",
#             {
#                 "title":title,
#                 "description":description,
#                 "content":content,
#                 "thumbnail":thumbnail,
#                 "date":date,
#                 "readTime":readTime,
#                 "category":category
#             },200)
#     except Exception as e:
#         print(f"Terjadi kesalahan saat memperbarui data {e}")
#         return response(f"Terjadi kesalahan saat memperbarui data.",[],500)
    
def deleteBlog(blog_id):
    authHeader(response=response)
    
    try:
        if not blog_id:
            return response("Blog id is required", [], 400)
        isExist = Blog.query.get(blog_id)
        if not isExist:
            return response("Blog is not defined", [], 404)
        
        isExist.tags.clear()
        db.session.commit()

        db.session.delete(isExist)
        db.session.commit()
        return response("Blog berhasil dihapus", {"rows":1}, 200)
    except Exception as e:
        db.session.rollback()
        print(f"Terjadi kesalahan saat menghapus data {e}")
        return response(f"Terjadi kesalahan saat menghapus blog", [], 500)
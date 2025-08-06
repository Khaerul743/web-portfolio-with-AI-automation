from flask import Blueprint
from app.controllers import blogController

blogRoute = Blueprint("blogRoute",__name__)

blogRoute.route("/api/blog",methods=["GET"])(blogController.getAllBlogDisplay)
blogRoute.route("/api/blog/<int:blog_id>",methods=["GET"])(blogController.getBlogById)
blogRoute.route("/api/blog",methods=["POST"])(blogController.addBlog)
# blogRoute.route("/api/blog/<blog_id>",methods=["PUT"])(blogController.updateBlog)
blogRoute.route("/api/blog/<int:blog_id>",methods=["DELETE"])(blogController.deleteBlog)
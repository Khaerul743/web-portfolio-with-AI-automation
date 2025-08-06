import axios from "../config/axios";

export async function fetchBlogs() {
  try {
    const response = await axios.get("http://localhost:5000/api/blog", {
      headers: {
        "agent-key": "erl_doiadnafkfsnsfkjnsfeionnb_fnfsoefnionfnsfkjdf"
      }
    });
    return response.data;
  } catch (error) {
    return { error: error.response?.data || error.message };
  }
}

export async function fetchBlogDetail(blogId) {
  try {
    const response = await axios.get(`http://localhost:5000/api/blog/${blogId}`, {
      headers: {
        "agent-key": "erl_doiadnafkfsnsfkjnsfeionnb_fnfsoefnionfnsfkjdf"
      }
    });
    return response.data;
  } catch (error) {
    return { error: error.response?.data || error.message };
  }
}

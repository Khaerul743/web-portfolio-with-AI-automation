from typing import List

def format_jurnal_list(jurnal_list:List) -> str:
    formatted = []
    for idx, jurnal in enumerate(jurnal_list, start=1):  # top 3
        formatted.append(
            f"""[{idx}]
Judul: {jurnal["title"]}
Tahun: {jurnal["year"]}
Diterbitkan oleh: {jurnal["publicationInfo"]}
Ringkasan: {jurnal["snippet"]}
Link PDF: {jurnal["pdfUrl"]}
"""
        )
    return "\n".join(formatted)

def tavily_format_result(results: list[dict]) -> str:
    """
    Format hasil pencarian menjadi teks rapi untuk dibaca agent.

    Parameters:
    - results: List hasil pencarian, setiap item memiliki 'url' dan 'content'

    Returns:
    - String yang diformat rapi untuk dikonsumsi oleh LLM
    """
    if not results:
        return "Tidak ditemukan hasil pencarian."

    formatted = "Berikut adalah ringkasan dari hasil pencarian:\n\n"
    for idx, item in enumerate(results, start=1):
        content = item.get("content", "").strip()
        url = item.get("url", "")
        formatted += f"{idx}. {content}\n   Sumber: {url}\n\n"

    return formatted.strip()

def gnews_format_result(results: list) -> str:
    formatted = ""
    for idx, item in enumerate(results, start=1):
        title = item.get("title", "").strip()
        description = item.get("description", "").strip()
        content = item.get("content", "").strip()
        url = item.get("url", "").strip()
        published = item.get("publishedAt", "").strip()

        formatted += (
            f"{idx}. Judul: {title or '-'}\n"
            f"   Deskripsi: {description or '-'}\n"
            f"   Konten: {content or '-'}\n"
            f"   URL: {url or '-'}\n"
            f"   Tanggal: {published or '-'}\n\n"
        )
    return formatted

def format_blog_body(body_results):
    result = ""
    for section in body_results:
        result += f"\n\n## {section.subtitle}\n\n"
        paragraphs = section.content.strip().split('\n\n')
        for para in paragraphs:
            result += para.strip() + "\n\n"
    return result.strip()

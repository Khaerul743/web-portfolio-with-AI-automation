from typing import List, Any, Optional, Annotated, Sequence, Dict, Union
from pydantic import Field, BaseModel
from langgraph.graph import add_messages
from langchain_core.messages import BaseMessage


class toolStructuredOutput(BaseModel):
    """Jurnal ilmiah terpilih"""
    title: str = Field(
        ...,
        description="Judul jurnal",
    )
    publicationInfo: str = Field(
        ...,
        description="info publish jurnal"
    )
    snippet: str = Field(
        ...,
        description="snippet jurnal"
    )
    year: int = Field(
        ...,
        description="Tahun publish jurnal"
    )
    pdfUrl: str = Field(
        ...,
        description="url pdf"
    )

class NextStepStructuredOutput(BaseModel):
    """Pengambilan keputusan"""
    search_again: bool = Field(
        ...,
        description="Apakah informasi yang didapatkan dari tools sudah cukup?"
    )
    recomendation: str = Field(
        ...,
        description="Rekomendasi tool yang akan dipakai berserta query nya"
    )
    reason: str = Field(
        ...,
        description="Alasan berdasarkan keputusan kamu"
    )

class TavilyFormat(BaseModel):
    """Format tavily search"""
    result: str = Field(
        ...,
        description="Hasil pencarian"
    )
    url: str = Field(
        ...,
        description="Sumber hasil pencarian berupa url"
    )

class HeaderStructuredOutput(BaseModel):
    """Header blog"""
    hook: str = Field(
        ...,
        description="Hook supaya user tertarik untuk membacanya"
    )
    purpose: str = Field(
        ...,
        description="Tujuan blog"
    )

class BodyResultFormat(BaseModel):
    """Subtitle dan konten body blog"""
    subtitle:str = Field(
        ...,
        description="Subtitle untuk setiap konten"
    )
    content:str = Field(
        ...,
        description="Isi konten"
    )
    
class BodyStructuredOutput(BaseModel):
    """Blog body"""
    body_result: List[BodyResultFormat] = Field(
        ...,
        description="Berisi kumpulan subtitle dan konten yang telah dibuat"
    )

class FooterStructuredOutput(BaseModel):
    "Footer blog"
    conclusion: str = Field(
        ...,
        description="Kesimpulan dari konten tersebut"
    )


class RevisionStructuredOutput(BaseModel):
    """Revision output"""
    valid: bool = Field(
        ...,
        description="Apakah sesuai?"
    )
    mistake: Optional[str] = Field(
        None,
        description="Kesalahan dari si agent dalam membuat blog (jika ada)"
    )
    repaired: Optional[str] = Field(
        None,
        description="Hal yang harus diperbaiki dari kesalahan tersebut (jika ada)"
    )

class SentimentStructuredOutput(BaseModel):
    """Sentiment analysis"""
    isAgree: bool = Field(
        ...,
        description="Apakah pesan dari user terlihat setuju?"
    )

class DetailBlogStructuredOutput(BaseModel):
    """Generate detail blog"""
    title: str = Field(
        ...,
        description="Judul yang cocok untuk blog tersebut"
    )
    headline: str = Field(
        ...,
        description="headline"
    )
    author: str = Field(
        ...,
        description="Pembuat blog (isi dengan 'My AI Agent')"
    )
    description: str = Field(
        ...,
        description="Deskripsi dari blog tersebut"
    )
    readTime: int = Field(
        ...,
        description="Perkiraan waktu untuk membaca blog ini (dalam satuan menit)"
    )
    tags: List[int] = Field(
        ...,
        description="Tags blog"
    )


class RevisionByHumanStructuredOutput(BaseModel):
    """Revision output"""
    mistake: Optional[str] = Field(
        None,
        description="Kesalahan dalam membuat blog."
    )
    repaired: Union[HeaderStructuredOutput, BodyStructuredOutput, FooterStructuredOutput] = Field(
        None,
        description="Hasil perbaikan dari kesalahan tersebut."
    )

    section_blog: str = Field(
        ...,
        description="Pilih salah satu bagian blog yang harus direvisi, bagian yang tersedia: header, body, footer "
    )

class AgentState(BaseModel):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    topic:str
    prompt:str
    tavily_message: str
    serper_message: str
    gNews_message: str
    wiki_message: str
    thumbnail: str
    search_again: Any
    search_recomendation:str
    header_result: Any = None
    body_result: Any = None
    footer_result: Any = None
    detail_blog: Any = None
    isValid: bool
    human_revision: str
    mistake: Any
    section_blog: Any
    revision_suggestion: Any
    retry: int

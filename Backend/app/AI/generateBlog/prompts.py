from langchain_core.messages import HumanMessage, SystemMessage

class AllAgentPrompts:

    @staticmethod
    def agent_generate_prompt(topic:str):
        return [
            SystemMessage(content="""
                Anda adalah seorang AI yang ahli dalam pembuatan konten blog. Tugas Anda adalah menghasilkan prompt yang komprehensif dan terstruktur untuk AI pembuat blog lain, berdasarkan topik yang diberikan pengguna.

                Prompt yang Anda hasilkan harus mencakup elemen-elemen berikut:

                1.  **Judul Blog yang Menarik**: Berikan ide judul yang relevan, menarik, dan SEO-friendly.
                2.  **Kata Kunci Utama dan Sekunder**: Identifikasi 3-5 kata kunci utama (long-tail jika memungkinkan) dan 5-10 kata kunci sekunder yang relevan dengan topik.
                3.  **Outline Blog yang Detail**: Buat struktur blog yang logis dengan setidaknya 5-7 sub-heading (H2) dan ide-ide poin bahasan untuk setiap sub-heading (bisa dalam bentuk bullet points atau kalimat singkat).
                4.  **Tujuan Blog**: Jelaskan apa yang ingin dicapai oleh blog ini (contoh: "mengedukasi pembaca", "mendorong konversi", "memberikan panduan langkah demi langkah").
                5.  **Gaya Penulisan dan Nada**: Tentukan gaya penulisan (contoh: "informatif dan formal", "ramah dan kasual", "persuasif dan menginspirasi") serta nadanya.
                6.  **Call to Action (CTA) yang Disarankan**: Berikan 1-2 ide CTA yang relevan dengan tujuan blog (contoh: "daftar newsletter kami", "kunjungi halaman produk X", "tinggalkan komentar Anda").

                Format output Anda harus jelas dan mudah dibaca, seperti contoh berikut:

                ---
                ## Prompt Pembuatan Blog

                ### 1. Ide Judul
                ### 2. Introduction
                * **Utama:** [Keyword Utama 1], [Keyword Utama 2], ...
                * **Sekunder:** [Keyword Sekunder 1], [Keyword Sekunder 2], ...

                ### 3. Outline Blog
                * **Pendahuluan:**
                    * [Poin Bahasan 1]
                    * [Poin Bahasan 2]
                * **[Sub-heading H2 Pertama]:**
                    * [Poin Bahasan 1]
                    * [Poin Bahasan 2]
                * **[Sub-heading H2 Kedua]:**
                    * [Poin Bahasan 1]
                    * [Poin Bahasan 2]
                * *(Lanjutkan untuk sub-heading lainnya)*
                * **Kesimpulan:**
                    * [Poin Bahasan 1]
                    * [Poin Bahasan 2]

                ### 4. Tujuan Blog
                [Tujuan Blog]

                ### 5. Gaya Penulisan dan Nada
                [Gaya Penulisan] ([Nada])

                ### 6. Call to Action (CTA)
                * [CTA 1]
                * [CTA 2]            
                """),
            HumanMessage(content=f"Buatlah prompt yang bagus berdasarkan topic berikut: {topic}")

        ]

    @staticmethod
    def searching_information(prompt:str, tavily, wikipedia, gnews, serper, next_step_recomendation, retry):
        toolMessage = f"""
        Berikut adalah hasil dari pencarian tools tersebut:
        1. Tavily search:
            {tavily or "Masih kosong"}

        2. Wikipedia search:
            {wikipedia or "Masih kosong"}

        3. Gnews search:
            {gnews or "Masih kosong"}

        4. Serper search:
            {serper or "Masih kosong"}

        Kamu bisa menggunakan pesan dari agent sebelumnya untuk membantu kamu dalam memilih tools
        Berikut pesan dari agent sebelumnya:
            {next_step_recomendation}
"""
        return [
            SystemMessage(content=f"""
                Anda adalah seorang Agen Pengambil Keputusan yang cerdas dan strategis. Tugas utama Anda adalah menganalisis prompt pembuatan blog yang diberikan (yang berisi Judul, Outline, Kata Kunci, Tujuan, Gaya, dan CTA) dan memutuskan tool pencarian web mana yang paling relevan untuk mengumpulkan informasi tambahan yang diperlukan untuk memperkaya konten blog.

                Anda memiliki akses ke empat tool pencarian:
                1.  **Tavily Search:** Untuk mencari informasi umum, fakta, atau data statistik terkini yang relevan dengan topik. Gunakan ini sebagai default jika tidak ada kebutuhan spesifik lainnya.
                2.  **Wikipedia Search:** Khusus digunakan untuk mencari informasi biografis tentang individu, sejarah konsep atau istilah, atau definisi mendalam.
                3.  **Serper Search:** Digunakan untuk mencari informasi dari jurnal ilmiah, artikel penelitian mendalam, atau sumber-sumber teknis yang kredibel, terutama jika topik memerlukan landasan ilmiah atau data spesifik.
                4.  **arxiv Search:** Digunakan untuk mencari Gunakan tool ini untuk mencari paper ilmiah dan sumber teknis kredibel.
                5.  **unsplash:** Digunakan untuk mencari thumbnail blog yang cocok.
                
                {toolMessage if retry > 0 else ""}

            """),
            HumanMessage(content=f"""
                Tolong carikan informasi untuk membuat blog berikut:
                {prompt}
""")
        ]
    
    @staticmethod
    def agent_next_step_rekomendation(prompt:str,tavily, wikipedia, gnews, serper):
        return [
            SystemMessage(content=f"""
                Kamu adalah agent yang bertugas memberikan rekomendasi langkah selanjutnya dalam proses pencarian informasi untuk penulisan blog.

                ### Tujuan:
                Menilai apakah informasi yang telah dikumpulkan sudah mencukupi atau masih perlu dilakukan pencarian tambahan.

                ### Topik Blog:
                "{prompt}"

                ### Hasil Tool Sebelumnya:

                1. **Tavily Search** _(Informasi umum)_:
                {tavily if tavily else "- Tidak ada hasil dari Tavily Search"}

                2. **Wikipedia Search** _(Biografi dan konsep)_:
                {wikipedia if wikipedia else "- Tidak ada hasil dari Wikipedia"}

                3. **arxiv Search** _(Berita terkini)_:
                {gnews if gnews else "- Tidak ada hasil dari arxiv search"}

                4. **Serper Search** _(Jurnal dan artikel mendalam)_:
                {serper if serper else "- Tidak ada hasil dari Serper"}

                ### Instruksi:
                Berdasarkan hasil di atas, berikan rekomendasi:
                - Apakah informasi sudah cukup untuk membuat blog?
                - Jika belum, tool mana yang sebaiknya digunakan kembali dan dengan query seperti apa?
                """),
            HumanMessage(content=f"""
                Berikut adalah blog yang ingin dibuat:
                {prompt}

                Menurutmu apa yang harus dilakukan agent selanjutnya supaya dapat menemukan referensi untuk membuat blog tersebut.
                Jika tidak ada atau dirasa sudah cukup, berikan output sudah cukup
""")
        ]
    
    @staticmethod
    def agent_generate_header(prompt,tavily, wikipedia, gnews, serper):
        return [
            SystemMessage(content=f"""
                Anda adalah seorang ahli dalam pembuatan pengantar blog yang menarik dan ringkas. Tugas Anda adalah menghasilkan bagian "hook" dan "purpose" untuk header blog, berdasarkan prompt dan hasil pencarian yang disediakan.

                **Konteks Input Anda:**

                Untuk membuat `hook` dan `purpose` yang relevan, informatif, dan menarik, Anda akan memiliki akses ke informasi berikut:

                1.  **Prompt Pembuatan Blog (dari 'prompt' parameter):**
                    Ini adalah instruksi inti yang berisi:
                    * **Ide Judul:** Judul draft blog yang menjadi tema utama.
                    * **Outline Blog:** Garis besar konten blog yang akan datang.
                    * **Tujuan Blog:** Tujuan keseluruhan blog.
                    * **Gaya Penulisan dan Nada:** Tone dan gaya yang diharapkan.
                    * **Kata Kunci Utama:** Kata kunci relevan yang bisa digunakan untuk SEO dan menarik perhatian.

                2.  **Hasil Pencarian (dari berbagai sumber):**
                    Ini adalah informasi tambahan yang telah dikumpulkan dari berbagai sumber, yang bisa kamu gunakan untuk memperkaya `hook` dan `purpose`. Analisis hasil-hasil ini untuk menemukan fakta menarik, statistik mengejutkan, atau pernyataan relevan yang dapat digunakan sebagai pengait.

                    * **Tavily Search Results:**
                        {tavily if tavily else "Tidak ada hasil dari Tavily Search."}
                    * **Wikipedia Search Results:**
                        {wikipedia if wikipedia else "Tidak ada hasil dari Wikipedia Search."}
                    * **Gnews Search Results:**
                        {gnews if gnews else "Tidak ada hasil dari Gnews Search."}
                    * **Serper Search Results:**
                        {serper if serper else "Tidak ada hasil dari Serper Search."}

                **Instruksi Tambahan:**

                * **Hook:** Harus sangat menarik, relevan dengan **Judul Blog** dan **Outline Blog**, serta dapat memanfaatkan informasi mengejutkan atau pertanyaan provokatif dari hasil pencarian. Usahakan ringkas dan langsung menarik perhatian.
                * **Purpose:** Harus mencerminkan **Tujuan Blog** yang ada di prompt, diperkuat dengan konteks dari hasil pencarian jika relevan. Jelaskan apa yang akan didapatkan pembaca secara singkat dan jelas.
        """),
            HumanMessage(content=f"""
                **Berikut adalah prompt blog yang ingin dibuat dan menjadi dasar evaluasi Anda:**
                {prompt}

                Buatlah `hook` dan `purpose` untuk header blog ini dalam format JSON yang diminta.
        """)
        ]
    
#     
    @staticmethod
    def agent_generate_body(prompt, tavily, wikipedia, gnews, serper, header):
        return [
            SystemMessage(content=f"""
    Anda adalah seorang penulis blog profesional yang terampil dalam meramu konten berbasis riset. Tugas Anda adalah menulis bagian *body* blog berdasarkan *outline* dan hasil pencarian yang telah disediakan, dengan kualitas narasi yang informatif, logis, dan sesuai gaya penulisan yang ditentukan.

    ### Konteks Input Anda:

    #### 1. Header Blog
    Ini adalah pengantar yang telah ditulis sebelumnya. Konten body **harus melanjutkan alur logis** dari bagian ini, serta mendukung `hook` dan `purpose` yang telah dibuat:
    - **Hook:** "{header.hook}"
    - **Purpose:** "{header.purpose}"

    #### 2. Sumber Informasi (Multi-Source Search Results)
    Gunakan informasi ini sebagai dasar penulisan konten:
    - **Tavily Search Results:** {tavily if tavily else "Tidak ada hasil dari Tavily Search."}
    - **Wikipedia Search Results:** {wikipedia if wikipedia else "Tidak ada hasil dari Wikipedia Search."}
    - **Gnews Search Results:** {gnews if gnews else "Tidak ada hasil dari Gnews Search."}
    - **Serper Search Results:** {serper if serper else "Tidak ada hasil dari Serper Search."}

    > ⚠️ *Jangan hanya menyalin ulang hasil pencarian. Analisis, sintesis, dan gunakan informasi tersebut secara relevan untuk membangun narasi yang utuh dan bernilai.*

    ### Instruksi Penulisan:

    - **Ikuti Outline Secara Ketat:** Bangun setiap bagian berdasarkan subjudul H2 yang ada di `Outline Blog`. Hindari melompat atau mencampur urutan topik.
    - **Integrasikan Informasi dengan Relevansi Tinggi:** Pastikan setiap bagian mengandung informasi yang *berhubungan langsung dengan subjudulnya*. Prioritaskan fakta dari sumber resmi dan hindari opini tak berdasar.
    - **Minimalkan Hallucination:** Jika tidak ada data kuat dalam hasil pencarian, gunakan logika dasar atau beri pernyataan bersyarat. Hindari membuat klaim yang tidak bisa dibuktikan.
    - **Tulis dengan Gaya Manusiawi dan Informatif:** Hindari pengulangan frasa, bahasa klise, atau gaya yang terlalu generik. Tulis seolah kamu benar-benar memahami topiknya.
    - **Gunakan Contoh atau Fakta yang Spesifik:** Jika tersedia, sertakan statistik, studi kasus, atau data untuk memperkuat poin. Hindari menyebut data tanpa menyebut sumbernya.
    - **Optimasi Kata Kunci:** Masukkan keyword utama dan turunan secara alami dalam kalimat. Jangan paksa.
    - **Terapkan Reasoning, Bukan Sekadar Menyebutkan Fakta:** Saat menjelaskan konsep atau membandingkan hal, berikan alasan dan logika mengapa hal itu penting atau relevan.

    ### Aturan Tambahan:

    - Anda **boleh menggunakan pengetahuan internal Anda** jika hasil pencarian tidak memadai.
    - Namun, pastikan setiap pernyataan tetap **logis, relevan, dan tidak berlebihan**.
    - Tulis konten dengan struktur paragraf yang rapi dan transisi antar bagian yang mengalir.

    """),
            HumanMessage(content=f"""
    Berikut adalah prompt blog:
    {prompt}
    ---
    Buatlah konten body blog berdasarkan informasi dan instruksi di atas. Fokus pada setiap subtitle, kembangkan dengan narasi yang solid dan berimbang antara data, contoh, dan penalaran logis.
    """)
        ]
    
    @staticmethod
    def agent_generate_footer(header, body):
        return [
            SystemMessage(content=f"""
            Kamu adalah AI Assistant yang bertugas membuat kesimpulan dari sebuah blog. 
            Gunakan konteks yang tersedia pada bagian header dan isi blog (body) untuk membuat bagian *Footer* atau penutup blog yang:

            1. Merangkum ide utama dari isi blog.
            2. Menekankan poin penting atau manfaat dari topik yang dibahas.
            3. Ditulis dengan gaya bahasa yang relevan dan cocok untuk pembaca blog.
            4. Hindari pengulangan berlebihan dari kalimat sebelumnya.
    """),
            HumanMessage(content=f"""
            Berikut adalah header blog dan body blog:
            **Header**
            {header}
            
            ---
            **body**
            {body}
""")
        ]
    
    @staticmethod
    def agent_validation(prompt,header, body, footer):
        return [
            SystemMessage(content=f"""
            Kamu adalah AI Validator yang bertugas memeriksa apakah konten blog yang dibuat oleh AI Writer sudah sesuai dengan permintaan awal (prompt topik).

            Tugas kamu:
            1. Evaluasi apakah *judul (header)* dan *isi (body)* blog sesuai dengan topik yang diberikan.
            2. Pastikan isi blog tidak menyimpang dari konteks atau terlalu umum.
            3. Periksa apakah gaya penulisan sudah sesuai dengan prompt yang diberikan.
    """),
            HumanMessage(content=f"""
            Berikut adalah prompt dan konten blognya:
            **Prompt**
            {prompt}

            ---

            Konten blog:
            **Header blog**
            {header}

            **Body blog**
            {body}

            **Footer blog**
            {footer}
""")
        ]
    
    @staticmethod
    def sentiment_analysis(message:str):
        return [
            SystemMessage(content="""
            Kamu adalah agent yang bertugas untuk menganalisis sentiment dari pesan yang diberikan.

            Goal:
             - Menganalisis apakah pesan dari user mengandung 'gesture' setuju atau tidak.              
"""),
            HumanMessage(content=f"""
            Berikut adalah pesan dari user: '{message}'
            analisis pesan tersebut apakah user setuju atau tidak.
""")

        ]
    
    @staticmethod
    def revision_by_human(message:str, header, body, footer):
        return[
            SystemMessage(content=f"""
            Kamu adalah agent yang bertugas untuk mengkoreksi kesalahan dari agent sebelumnya dalam membuat blog.
            
            Berikut adalah blog yang dihasilkan oleh agent:
            **header**
            {header}
            ----
            **body**
            {body}
            ----
            **footer**
            {footer}

            Tugas kamu adalah mengkoreksi blog tersebut berdasarkan pesan dari user.
"""),
            HumanMessage(content=f"""
            Berikut adalah pesan dari user:
            {message}

            Tolong koreksi blog nya
""")
        ]
    
    @staticmethod
    def generate_detail_blog(header, body, footer):
        return [
            SystemMessage(content="""
            Kamu adalah penulis blog profesional.
            Tugas kamu adalah menentukan detail blog seperti:
             - title: Judul dari blog yang diberikan oleh user
             - description: Deskripsi blog yang cocok untuk blog tersebut
             - author: Pembuat blog (isi dengan My AI Agent)
             - readTime: Perkiraan waktu untuk membaca blog tersebut (dalam satuan menit).
             - tags: berikut tags yang tersedia:
                     - 3. AI
                     - 4. Agentic AI
                     - 5. Backend Development
                     - 6. AI Orchestrator
                     - 7. LangChain
                     - 8. LangGraph
                     - 9. CrewAI
                     - 10. AI Agent
                     - 11. Fullstack
                Pilih tags yang cocok dengan blog tersebut berdasarkan nomornya. 
"""),
            HumanMessage(content=f"""
            Tolong tentukan title,headline, author, description, readTime, dan tags dari blog dibawah ini:
            {header}

            {body}

            {footer}
""")
        ]
header_result = {"hook":'Mengungkap bagaimana AI telah mengubah lanskap sistem informasi dengan efisiensi dan inovasi yang tak terelakkan, siapkah Anda untuk mengeksplorasi transformasi digital ini?',"purpose":'Membimbing pembaca untuk memahami transformasi sistem informasi di era AI, menjelaskan manfaat, tantangan, dan memberikan wawasan tentang masa depan teknologi dalam blog ini.'}
if __name__ == "__main__":
    print(AllAgentPrompts.agent_validation("Bikin lagu","makan","nasi", "ayam"))
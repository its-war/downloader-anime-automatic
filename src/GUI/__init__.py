import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from src import downloader

driver = webdriver.Chrome()


def pesquisar(event=None):
    nome_anime = input_anime_search.get()
    main_label.focus_set()
    animes = downloader.search_anime(driver, nome_anime)

    limpar_resultados()

    for i, anime in enumerate(animes):
        label = tk.Label(scrollable_frame, text=anime['nome'])
        label.grid(row=i, column=0, padx=5, pady=5)

        btn = tk.Button(scrollable_frame, text='Baixar',
                        command=lambda link=anime['download'], nome=anime['nome']: abrir_anime(link, nome))
        btn.grid(row=i, column=1, padx=5, pady=5)


def abrir_anime(link, nome):
    episodios = downloader.get_episodios_list(driver, link)
    for ep in episodios:
        downloader.download_video(driver, ep['link'])
    downloader.esperar_download_completo(driver)
    messagebox.showinfo('Download concluído!', f'Os episódios de {nome} foram baixados.')


def limpar_resultados():
    for widget in scrollable_frame.winfo_children():
        widget.destroy()


def on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")


janela = tk.Tk()
janela.title('AniTube Downloader')
janela.geometry("900x450")

main_label = tk.Label(janela, text="Pesquise o nome do anime...")
main_label.grid(row=0, column=0, padx=5, pady=5)

input_anime_search = tk.Entry(janela, width=100)
input_anime_search.grid(row=0, column=1, padx=5, pady=5)
input_anime_search.bind("<Return>", pesquisar)

frame_resultados = tk.Frame(janela)
frame_resultados.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

canvas = tk.Canvas(frame_resultados, width=870, height=410)
scrollbar = tk.Scrollbar(frame_resultados, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

canvas.bind_all("<MouseWheel>", on_mousewheel)


def iniciar_janela():
    janela.mainloop()

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

canvas_sac = None
canvas_price = None  

def sac(valor_casa, taxa_de_juros, num_parcelas):
    amortizacao = valor_casa / num_parcelas
    juros_total = 0
    total_pago = 0
    parcelas = []
    saldo_devedor = valor_casa

    for i in range(num_parcelas):
        juros = saldo_devedor * (taxa_de_juros / 100)
        mensalidade = amortizacao + juros
        saldo_devedor -= amortizacao
        total_pago += mensalidade
        parcelas.append((i, mensalidade, juros, amortizacao, saldo_devedor))

    return parcelas, sum([parcela[2] for parcela in parcelas]), total_pago

def price(valor_casa, taxa_de_juros, num_parcelas):
    taxa_de_juros_decimal = taxa_de_juros / 100
    prestacao = valor_casa * (taxa_de_juros_decimal * (1 + taxa_de_juros_decimal) ** num_parcelas) / ((1 + taxa_de_juros_decimal) ** num_parcelas - 1)
    juros_total = 0
    total_pago = 0
    saldo_devedor = valor_casa
    parcelas = []

    for i in range(num_parcelas):
        juros = saldo_devedor * taxa_de_juros_decimal
        amortizacao = prestacao - juros
        saldo_devedor -= amortizacao
        parcelas.append((i, prestacao, juros, amortizacao, saldo_devedor))
        total_pago += prestacao
        juros_total += juros

    return parcelas, juros_total, total_pago

def Calcular_financiamento(event=None):
    global canvas_sac
    global canvas_price

    nome = str(entry_nome.get())
    salario = float(entry_salario.get())
    valor_casa = float(entry_valor_casa.get())
    taxa_de_juros_str = entry_taxa_juros.get()
    num_parcelas = int(entry_num_parcelas.get()) *12
    taxa_de_juros = float(taxa_de_juros_str.rstrip('%'))

    limite_mensalidade = 0.3 * salario
    tipo_de_amortizacao = entry_amortizacao.get()

    if tipo_de_amortizacao in ['sac', 'price']:
        parcelas_sac, juros_total_sac, total_pago_sac = sac(valor_casa, taxa_de_juros, num_parcelas)
        parcelas_price, juros_total_price, total_pago_price = price(valor_casa, taxa_de_juros, num_parcelas)

        resultado_popup = tk.Toplevel()
        if tipo_de_amortizacao == 'sac':
            resultado_popup.title('Resultado SAC')
            parcelas, juros_total, total_pago = parcelas_sac, juros_total_sac, total_pago_sac
        else:
            resultado_popup.title('Resultado Price')
            parcelas, juros_total, total_pago = parcelas_price, juros_total_price, total_pago_price

        resultado_popup.geometry('400x300')
        resultado_popup.resizable(True, True)

        frame = tk.Frame(resultado_popup)
        frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(frame)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

        content_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=content_frame, anchor='nw')

        mensalidade = total_pago / num_parcelas
        if mensalidade > limite_mensalidade:
            salario_minimo_necessario = mensalidade / 0.3
            messagebox.showerror('Erro', f'O valor da mensalidade excede 30% do salário mensal. O salário mínimo necessário é de R$ {salario_minimo_necessario:.2f}.')
            return

        mostrar_resultado(nome, parcelas, juros_total, total_pago, tipo_de_amortizacao, content_frame)

        def scroll(event):
            if tipo_de_amortizacao == 'sac':
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            else:
                canvas_price.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", scroll)

    elif tipo_de_amortizacao == '0':
        parcelas_sac, juros_total_sac, total_pago_sac = sac(valor_casa, taxa_de_juros, num_parcelas)
        parcelas_price, juros_total_price, total_pago_price = price(valor_casa, taxa_de_juros, num_parcelas)

        resultado_sac = tk.Toplevel()
        resultado_sac.title('Resultado SAC')
        resultado_sac.geometry('400x300')
        resultado_sac.resizable(True, True)

        resultado_price = tk.Toplevel()
        resultado_price.title('Resultado Price')
        resultado_price.geometry('400x300')
        resultado_price.resizable(True, True)

        frame_sac = tk.Frame(resultado_sac)
        frame_sac.pack(fill=tk.BOTH, expand=True)

        frame_price = tk.Frame(resultado_price)
        frame_price.pack(fill=tk.BOTH, expand=True)

        canvas_sac = tk.Canvas(frame_sac)
        canvas_sac.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar_sac = ttk.Scrollbar(frame_sac, orient=tk.VERTICAL, command=canvas_sac.yview)
        scrollbar_sac.pack(side=tk.RIGHT, fill=tk.Y)

        canvas_sac.configure(yscrollcommand=scrollbar_sac.set)

        canvas_sac.bind('<Configure>', lambda e: canvas_sac.configure(scrollregion=canvas_sac.bbox('all')))

        canvas_price = tk.Canvas(frame_price)
        canvas_price.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar_price = ttk.Scrollbar(frame_price, orient=tk.VERTICAL, command=canvas_price.yview)
        scrollbar_price.pack(side=tk.RIGHT, fill=tk.Y)

        canvas_price.configure(yscrollcommand=scrollbar_price.set)

        canvas_price.bind('<Configure>', lambda e: canvas_price.configure(scrollregion=canvas_price.bbox('all')))

        sac_frame = tk.Frame(canvas_sac)
        canvas_sac.create_window((0, 0), window=sac_frame, anchor='nw')

        price_frame = tk.Frame(canvas_price)
        canvas_price.create_window((0, 0), window=price_frame, anchor='nw')

        mensalidade_sac = total_pago_sac / num_parcelas
        mensalidade_price = total_pago_price / num_parcelas
        if mensalidade_sac > limite_mensalidade or mensalidade_price > limite_mensalidade:
            salario_minimo_necessario_sac = mensalidade_sac / 0.3
            salario_minimo_necessario_price = mensalidade_price / 0.3
            messagebox.showerror('Erro', f'O valor da mensalidade excede 30% do salário mensal. O salário mínimo necessário para SAC é de R$ {salario_minimo_necessario_sac:.2f} e para Price é de R$ {salario_minimo_necessario_price:.2f}.')
            return

        mostrar_resultado(nome, parcelas_sac, juros_total_sac, total_pago_sac, "SAC", sac_frame)
        mostrar_resultado(nome, parcelas_price, juros_total_price, total_pago_price, "Price", price_frame)

        def scroll(event):
            canvas_sac.yview_scroll(-1 * (event.delta // 120), "units")         
            canvas_price.yview_scroll(-1 * (event.delta // 120), "units")
        
        canvas_sac.bind_all("<MouseWheel>", scroll)
        canvas_price.bind_all("<MouseWheel>", scroll)

    else:
        messagebox.showerror('Erro', 'Opção de modelo de amortização inválida. Por favor, escolha "sac", "price" ou "0".')

def mostrar_resultado(nome, parcelas, juros_total, total_pago, tipo, frame=None):
    mensagem = f'{nome}, modelo {tipo} (para financiamento de casa):\n'
    mensagem += f'{"N°":<10}{"Prestação":<20}{"Juros":<20}{"Amortização":<20}{"Saldo devedor":<20}\n'
    for i, (numero, prestacao, juros, amortizacao, saldo_devedor) in enumerate(parcelas, start=0):
        mensagem += f'{numero:<10}R$ {prestacao:.2f}{" " * 8}R$ {juros:.2f}{" " * 8}R$ {amortizacao:.2f}{" " * 8}R$ {saldo_devedor:.2f}\n'
    mensagem += f'total de juros: R$ {juros_total:.2f}\n'
    mensagem += f'o valor que você pagará no total será de R$ {total_pago:.2f}\n'

    if frame:
        label = tk.Label(frame, text=mensagem, justify=tk.LEFT)
        label.pack(fill=tk.BOTH, expand=True)
        frame.update_idletasks()
    else:
        messagebox.showinfo('Resultado', mensagem)

app = tk.Tk()
app.title('Calculadora de Financiamento')

frame = tk.Frame(app)
frame.pack(padx=10, pady=10)

tk.Label(frame, text='Nome: ').grid(row=0, column=0, sticky='w')
entry_nome = tk.Entry(frame)
entry_nome.grid(row=0, column=1)

tk.Label(frame, text='Salário mensal: ').grid(row=1, column=0, sticky='w')
entry_salario = tk.Entry(frame)
entry_salario.grid(row=1, column=1)

tk.Label(frame, text='Valor do imóvel: ').grid(row=2, column=0, sticky='w')
entry_valor_casa = tk.Entry(frame)
entry_valor_casa.grid(row=2, column=1)

tk.Label(frame, text='Taxa de juros ao mes (1.0 = 1%): ').grid(row=3, column=0, sticky='w')
entry_taxa_juros = tk.Entry(frame)
entry_taxa_juros.grid(row=3, column=1)

tk.Label(frame, text='tempo de financiamento em anos: ').grid(row=4, column=0, sticky='w')
entry_num_parcelas = tk.Entry(frame)
entry_num_parcelas.grid(row=4, column=1)

tk.Label(frame, text='Modelo de amortização(sac, price ou 0): ').grid(row=5, column=0, sticky='w')
entry_amortizacao = tk.Entry(frame)
entry_amortizacao.grid(row=5, column=1)

calcular_button = tk.Button(frame, text='Calcular', command=Calcular_financiamento)
calcular_button.grid(row=6, columnspan=2)

app.bind('<Return>', Calcular_financiamento)

app.mainloop()

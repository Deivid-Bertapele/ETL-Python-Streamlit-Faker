import pandas as pd
import random
from faker import Faker

fake = Faker()

def generate_fake_data(n=1000):
    data = []
    for _ in range(n):
        produto = fake.word()
        artigocor = fake.color_name()
        cod_cota = fake.random.choice(["110", "125", "225", "425"])
        colecao = fake.word()
        tamanho = random.choice(["P", "M", "G", "GG"])
        categoria = fake.word()
        piramide = fake.word()
        grupo = fake.word()
        negocio = fake.word()
        subnegocios = fake.word()
        loja_propria = fake.boolean()
        quantidade_item = fake.random_int(min=1, max=100)
        quantidade_unitario = fake.random_int(min=1, max=50)
        margem_real = round(random.uniform(10, 50), 2)
        margem_percentual = round(random.uniform(5, 30), 2)
        preco_venda = round(random.uniform(10, 500), 2)
        receita_total = round(preco_venda * quantidade_item, 2)
        pecas_total = quantidade_item * quantidade_unitario

        data.append([
            produto, artigocor, cod_cota, colecao, tamanho, categoria, piramide,
            grupo, negocio, subnegocios, loja_propria, quantidade_item,
            quantidade_unitario, margem_real, margem_percentual, preco_venda,
            receita_total, pecas_total
        ])
    
    columns = [
        "Produto", "ArtigoCor", "Cod Cota", "Coleção", "Tamanho", "Categoria", "Piramide",
        "Grupo", "Negocio", "Subnegocios", "Loja Propria", "Quantidade Item",
        "Quantidade Unitário", "Margem Real", "Margem Percentual", "Preço Venda",
        "Receita Total", "Peças Total"
    ]
    return pd.DataFrame(data, columns=columns)

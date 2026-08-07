# -*- coding: utf-8 -*-
"""Gera fixtures.json com os mesmos dados DEMO que estão no Supabase,
para o Playwright poder testar sem rede."""
import json

PROD = [
 ("Adaptiv 15ml","Blend calma — PV 49.5",52.72,70.29,2),
 ("Air 15ml","Blend respiratório — PV 34.5",36.95,49.26,2),
 ("AromaTouch 15ml","Blend massagem — PV 39",41.86,55.81,2),
 ("Balance 15ml","Blend equilíbrio — PV 29",31.27,41.68,2),
 ("Basil 15ml","Manjericão — PV 34",36.43,48.57,2),
 ("Bergamot 15ml","Bergamota — PV 47.5",50.91,67.88,2),
 ("Cilantro 15ml","Coentro — PV 31",33.33,44.44,2),
 ("Deep Blue 5ml","Blend muscular — PV 42.5",45.47,60.63,2),
 ("Difusor","Lote 50 un. — capital: Marcio €1.046 (produto) + Sócio €150 (embalagens). Custo/venda: €20,92 produto + €3,00 embalagem = €23,92",23.92,170.00,5),
 ("Eucalyptus 15ml","Eucalipto — PV 22.5",24.29,32.39,2),
 ("Frankincense 15ml","Incenso — PV 92",98.71,131.61,2),
 ("Geranium 15ml","Gerânio — PV 56.5",60.73,80.97,2),
 ("Ginger 15ml","Gengibre — PV 59",63.31,84.41,2),
 ("Lavender 15ml","Lavanda — PV 36",38.24,50.98,2),
 ("Lemon 15ml","Limão — PV 17.5",18.61,24.81,2),
 ("Marjoram 15ml","Manjerona — PV 28",29.46,39.27,2),
 ("Melissa 5ml","Melissa — PV 135",142.64,190.19,1),
 ("On Guard 15ml","Blend proteção — PV 43.5",46.78,62.37,2),
 ("Oregano 15ml","Orégão — PV 34.5",36.95,49.26,2),
 ("Peppermint 15ml","Hortelã-pimenta — PV 29.5",31.78,42.37,2),
 ("Rosemary 15ml","Alecrim — PV 24",25.58,34.11,2),
 ("Serenity 15ml","Blend descanso — PV 47",50.39,67.19,2),
 ("Tea Tree 15ml","Melaleuca — PV 28",30.23,40.31,2),
 ("Thyme 15ml","Tomilho — PV 39",42.12,56.15,2),
 ("Zendocrine 15ml","Blend detox — PV 32.5",34.88,46.51,2),
 ("ZenGest 15ml","Blend digestivo — PV 41.5",44.44,59.25,2),
]
pid = {n: f"p{i:02d}" for i,(n,*_ ) in enumerate(PROD)}
produtos = [{"id":pid[n],"nome":n,"descricao":d,"custo_unit":c,"preco_venda":v,
             "estoque_minimo":m,"ativo":True,"created_at":"2026-07-27T14:44:39Z"}
            for n,d,c,v,m in PROD]
custo = {n:c for n,d,c,v,m in PROD}

CLI = [
 ("Ana Ribeiro","Aninha","whatsapp","+351 912 345 678","[DEMO] Cliente fiel, compra todos os meses"),
 ("Beatriz Nunes","Bea","whatsapp","+351 927 888 444","[DEMO]"),
 ("Carla Duarte",None,"outro",None,"[DEMO] Chegou por indicacao"),
 ("Miguel Pinto",None,"telegram","@mpinto","[DEMO] Sensivel ao preco"),
 ("Rui Almeida",None,"telegram","@ruialmeida","[DEMO] Sem contacto telefonico"),
 ("Sofia Marques","Sofi","whatsapp","+351 936 111 222","[DEMO] Amiga da Ana"),
 ("Tiago Sousa","tiago","telegram","@tiagosousa","[DEMO] So Telegram, nao sabemos o numero"),
]
cid = {n: f"c{i:02d}" for i,(n,*_ ) in enumerate(CLI)}
clientes = [{"id":cid[n],"nome":n,"apelido":a,"canal":ca,"contacto":ct,"notas":nt,
             "created_at":"2026-08-05T01:23:57Z"} for n,a,ca,ct,nt in CLI]

PEDIDOS = [
 ("Rui Almeida","2026-08-05","pendente",0,"3 difusores para o escritorio [DEMO]",[("Difusor",3,150.00)]),
 ("Sofia Marques","2026-08-04","pendente",0,"A aguardar pagamento MBWay [DEMO]",[("Frankincense 15ml",1,131.61),("Lavender 15ml",1,50.98)]),
 ("Tiago Sousa","2026-08-03","entregue",4,"[DEMO]",[("Peppermint 15ml",2,42.37)]),
 ("Carla Duarte","2026-08-02","pago",0,"Indicada pela Ana [DEMO]",[("Difusor",1,170.00)]),
 ("Ana Ribeiro","2026-08-01","entregue",0,"Repeticao [DEMO]",[("Balance 15ml",1,41.68),("Lemon 15ml",2,24.81)]),
 ("Miguel Pinto","2026-07-28","cancelado",0,"Desistiu, preco alto [DEMO]",[("Frankincense 15ml",1,131.61)]),
 ("Beatriz Nunes","2026-07-22","entregue",0,"Levou 2 difusores [DEMO]",[("Difusor",2,160.00),("Lavender 15ml",1,50.98)]),
 ("Rui Almeida","2026-07-19","pago",0,"Combinar entrega [DEMO]",[("Deep Blue 5ml",1,60.63)]),
 ("Sofia Marques","2026-07-12","entregue",5,"Desconto de amiga [DEMO]",[("On Guard 15ml",1,62.37),("Peppermint 15ml",1,42.37)]),
 ("Tiago Sousa","2026-07-08","entregue",0,"Primeiro difusor [DEMO]",[("Difusor",1,170.00)]),
 ("Ana Ribeiro","2026-07-03","entregue",0,"Entrega em Cascais [DEMO]",[("Lavender 15ml",2,50.98),("Lemon 15ml",1,24.81)]),
]
pedidos, movs, k = [], [], 0
for j,(cl,dt,est,desc,nt,itens) in enumerate(PEDIDOS):
    oid=f"o{j:02d}"; its=[]
    for it_n,q,pr in itens:
        k+=1
        its.append({"id":f"i{k:03d}","pedido_id":oid,"produto_id":pid[it_n],
                    "qtd":q,"preco_unit":pr,"custo_unit":custo[it_n]})
        if est!="cancelado":
            movs.append({"id":f"mv{k:03d}","produto_id":pid[it_n],"tipo":"venda","qtd":-q,
                         "custo_unit":custo[it_n],"pedido_id":oid,"data":dt,
                         "notas":"[DEMO] Venda","created_at":dt+"T10:00:00Z"})
    pedidos.append({"id":oid,"cliente_id":cid[cl],"data":dt,"estado":est,"desconto":desc,
                    "notas":nt,"created_at":dt+"T10:00:00Z","oleos_pedido_itens":its})

COMPRAS = [("Lavender 15ml",12,"2026-06-18"),("Lemon 15ml",12,"2026-06-18"),
           ("Peppermint 15ml",10,"2026-06-18"),("On Guard 15ml",10,"2026-06-18"),
           ("Deep Blue 5ml",6,"2026-07-10"),("Frankincense 15ml",4,"2026-07-10"),
           ("Balance 15ml",8,"2026-07-10")]
OUTROS = [("Lavender 15ml","brinde",-1,"2026-07-14","[DEMO] Brinde a Ana pela indicacao"),
          ("Peppermint 15ml","consumo_proprio",-1,"2026-07-25","[DEMO] Consumo proprio - Marcio"),
          ("Lavender 15ml","consumo_proprio",-1,"2026-08-02","[DEMO] Consumo proprio - socio"),
          ("On Guard 15ml","perda",-1,"2026-07-30","[DEMO] Frasco partido no transporte")]
for i,(n,q,d) in enumerate(COMPRAS):
    movs.append({"id":f"mc{i}","produto_id":pid[n],"tipo":"compra","qtd":q,"custo_unit":custo[n],
                 "pedido_id":None,"data":d,"notas":"[DEMO] Encomenda doTERRA","created_at":d+"T09:00:00Z"})
for i,(n,t,q,d,nt) in enumerate(OUTROS):
    movs.append({"id":f"mo{i}","produto_id":pid[n],"tipo":t,"qtd":q,"custo_unit":custo[n],
                 "pedido_id":None,"data":d,"notas":nt,"created_at":d+"T09:00:00Z"})
movs.append({"id":"mlote","produto_id":pid["Difusor"],"tipo":"compra","qtd":50,"custo_unit":20.92,
             "pedido_id":None,"data":"2026-07-28","notas":"Lote inicial — capital 100% Marcio (€1.046)",
             "created_at":"2026-07-28T09:00:00Z"})
movs.sort(key=lambda m: m["created_at"], reverse=True)

despesas = [
 {"id":"d1","categoria":"frete","descricao":"[DEMO] Portes CTT","valor":14.40,"data":"2026-08-04","created_at":""},
 {"id":"d2","categoria":"outros","descricao":"[DEMO] Etiquetas e fita","valor":12.90,"data":"2026-08-02","created_at":""},
 {"id":"d3","categoria":"frete","descricao":"[DEMO] Portes CTT - 6 encomendas","valor":21.60,"data":"2026-07-16","created_at":""},
 {"id":"d4","categoria":"sacos","descricao":"[DEMO] 100 sacos de papel kraft","valor":28.50,"data":"2026-07-05","created_at":""},
 {"id":"d5","categoria":"brindes","descricao":"[DEMO] 20 amostras 2ml para oferta","valor":34.00,"data":"2026-07-05","created_at":""},
]

estoque = {}
for m in movs:
    estoque[m["produto_id"]] = estoque.get(m["produto_id"],0) + m["qtd"]
v_estoque = [{"produto_id":p["id"],"nome":p["nome"],"estoque_minimo":p["estoque_minimo"],
              "ativo":True,"estoque":estoque.get(p["id"],0)} for p in produtos]

fx = {
 "oleos_socios":[{"email":"correa.marcio1@gmail.com","nome":"Marcio","created_at":"2026-07-27T13:38:24Z"}],
 "oleos_produtos":produtos,
 "oleos_precos_volume":[{"id":"t1","produto_id":pid["Difusor"],"qtd_min":2,"preco_unit":160.00},
                        {"id":"t2","produto_id":pid["Difusor"],"qtd_min":3,"preco_unit":150.00}],
 "oleos_clientes":clientes,
 "oleos_pedidos":pedidos,
 "oleos_mov_estoque":movs,
 "oleos_despesas":despesas,
 "oleos_v_estoque":v_estoque,
}
json.dump(fx, open("fixtures.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("fixtures.json:", {k:len(v) for k,v in fx.items()})
print("estoque:", {p["nome"]:p["estoque"] for p in v_estoque if p["estoque"]})

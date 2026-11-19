"""Gera o site estático Bambu Ubatuba em 3 idiomas (pt-BR, en, es).

Uso:  python3 tools/build.py
Saída: site/index.html, site/en/index.html, site/es/index.html, site/sitemap.xml, site/robots.txt

Edite as CONFIGURAÇÕES abaixo (domínio, links, avaliações) e rode o script novamente.
As fotos são geradas por tools/optimize_images.py (que cria tools/images.json).
"""
import json
import math
import os
from datetime import date
from html import escape
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")

# ============================ CONFIGURAÇÕES ============================
SITE_URL = "https://www.bambuubatuba.com.br"   # <- troque pelo domínio definitivo (sem barra no final)
WHATSAPP = "5535988275400"
INSTAGRAM = "https://www.instagram.com/bambu.ubatuba/"
MAPS = {  # links "Compartilhar" do Google com a localização de cada prédio
    "bambu": "https://www.google.com/maps/place/Bambu/data=!4m2!3m1!1s0x0:0x7f6db0caf002046f",
    "dna": "https://www.google.com/maps/place/Reserva+DNA/data=!4m2!3m1!1s0x0:0x9087ddb800ce647",
}
MAP_EMBED = "https://maps.google.com/maps?q=" + quote("Praia Grande, Ubatuba - SP") + "&z=14&output=embed"

APTS = [
    {"key": "bambu-202", "name": "Bambu 202", "condo": "bambu", "airbnb": "https://www.airbnb.com.br/rooms/819816502817753016",
     "rating": 5.0, "reviews": 40, "fav": True, "top1": True, "guests": 6, "bedrooms": 2, "beds": 4, "baths": 2, "parking": 1,
     "cats": [5.0, 5.0, 5.0, 5.0, 5.0, 4.9]},
    {"key": "bambu-410", "name": "Bambu 410", "condo": "bambu", "airbnb": "https://www.airbnb.com.br/rooms/820135919681995540",
     "rating": 4.96, "reviews": 25, "fav": True, "top1": False, "guests": 6, "bedrooms": 2, "beds": 4, "baths": 2, "parking": 1,
     "cats": [5.0, 5.0, 5.0, 5.0, 5.0, 4.9]},
    {"key": "reserva-dna", "name": "Reserva DNA 14.4.1", "condo": "dna", "airbnb": "https://www.airbnb.com.br/rooms/913872230965185636",
     "rating": 4.93, "reviews": 15, "fav": False, "top1": False, "guests": 6, "bedrooms": 2, "suites": True, "beds": 4, "baths": 3, "social": 1, "parking": 2,
     "cats": [4.9, 4.9, 4.8, 5.0, 4.6, 4.7]},
]

# Avaliações em destaque: cole aqui as melhores avaliações reais do Airbnb.
# Enquanto a lista estiver vazia, o bloco de depoimentos não aparece no site.
# Exemplo:
# {"name": "Mariana", "from": "São Paulo, SP", "date": "Out 2026", "apt": "Bambu 202",
#  "text": {"pt": "Texto original...", "en": "English translation...", "es": "Traducción..."}},
REVIEWS = []
# ======================================================================

LANGS = ["pt", "en", "es"]
HREFLANG = {"pt": "pt-BR", "en": "en", "es": "es"}
PATH = {"pt": "/", "en": "/en/", "es": "/es/"}
PREFIX = {"pt": "", "en": "../", "es": "../"}
OG_LOCALE = {"pt": "pt_BR", "en": "en_US", "es": "es_ES"}

T = {
"pt": {
 "title": "Apartamentos para Locação em Ubatuba Frente ao Mar | Bambu",
 "desc": "Locação por temporada em Ubatuba, na Praia Grande: apartamentos de alto padrão para aluguel frente ao mar, com piscina de borda infinita e lazer de resort. Anfitrião Superhost, +1.000 hospedagens. Reserve pelo WhatsApp.",
 "skip": "Pular para o conteúdo",
 "nav": ["Apartamentos", "Lazer", "Avaliações", "Localização", "Dúvidas"],
 "menu": "Abrir menu", "wa_short": "WhatsApp", "wa_btn": "Reservar pelo WhatsApp",
 "wa_msg": "Olá! Vi o site do Bambu Ubatuba e gostaria de consultar disponibilidade.",
 "wa_apt": "Olá! Tenho interesse no apartamento {apt}. Gostaria de consultar disponibilidade para as datas: ",
 "eyebrow": "Praia Grande · Ubatuba · SP",
 "h1": "Apartamentos <em>frente ao mar</em> em Ubatuba",
 "lead": "Locação por temporada de alto padrão na Praia Grande, Litoral Norte de São Paulo.<br>Apartamentos novos e decorados, com vista para o mar em condomínios com estrutura de lazer completa: piscina de borda infinita, piscina aquecida, sauna e academia.",
 "see_apts": "Ver apartamentos",
 "chip_rating": "5,0 no Airbnb", "chip_super": "Superhost", "chip_fav": "Preferido dos hóspedes",
 "trust": [("+1.000", "hospedagens realizadas"), ("Superhost", "anfitrião reconhecido no Airbnb"), ("Top 1%", "Preferido dos hóspedes no Airbnb"), ("1 hora", "tempo médio de resposta")],
 "apts_eyebrow": "Os apartamentos", "apts_h2": "Apartamentos para locação <em>em Ubatuba</em>",
 "apts_p": "Aluguel de temporada direto com o anfitrião. Apartamentos que acomodam até 6 hóspedes, com suíte, ar-condicionado em todos os ambientes, varanda gourmet e vaga de garagem.",
 "condo": {"bambu": "Condomínio Bambu · Vista mar", "dna": "Reserva DNA Resort · Frente mar"},
 "reviews_word": "avaliações", "see_airbnb": "Ver no Airbnb", "photos": "Ver as {n} fotos",
 "fav_badge": "Preferido dos hóspedes", "top1": "Top 1% do Airbnb",
 "spec": {"suites": "suítes", "social": "+ 1 social", "guests": "hóspedes", "bedrooms": "quartos", "beds": "camas", "baths": "banheiros", "parking_1": "vaga", "parking_n": "vagas", "ac": "em todos os quartos"},
 "ac": "Ar-cond.",
 "apt_desc": {
  "bambu-202": "Apartamento novo e totalmente decorado de frente para o mar da Praia Grande. Varanda gourmet com vista, cozinha completa, suíte com cama queen, quarto com duas camas de solteiro e sofá-cama na sala.",
  "bambu-410": "No 4º andar, com uma das vistas mais bonitas do prédio: mar, montanhas e a orla da Praia Grande. Moderno, completo e decorado, com varanda gourmet, suíte com cama queen e quarto com duas camas.",
  "reserva-dna": "Um verdadeiro resort à beira-mar.<br>Amplo, confortável, com 2 suítes, varanda gourmet com churrasqueira e vista para o jardim, suíte com cama queen e 2 vagas de garagem.",
 },
 "apt_hl": {
  "bambu-202": ["Vista para o mar", "Varanda gourmet", "Piscina de borda infinita", "Wi-Fi"],
  "bambu-410": ["Vista mar e montanhas", "Varanda gourmet", "Piscina aquecida", "Wi-Fi"],
  "reserva-dna": ["Churrasqueira na varanda", "2 suítes", "Cinema e hidromassagem", "Wi-Fi"],
 },
 "lz_eyebrow": "Lazer completo", "lz_h2": "Lazer de <em>resort</em> à beira-mar",
 "lz_p": "Os dois condomínios oferecem lazer para todas as idades, para você aproveitar Ubatuba mesmo nos dias de chuva.",
 "condos": {
  "bambu": ("Condomínio Bambu", "Prédio novo de frente para a Praia Grande, com rooftop e piscina de borda infinita olhando para o mar. Abriga os apartamentos 202 e 410."),
  "dna": ("Reserva DNA Resort", "Resort frente ao mar com jardins, várias piscinas, rooftop e lazer completo para a família. Abriga o apartamento 14.4.1."),
 },
 "amen": {
  "bambu": ["Piscina de borda infinita", "Piscina infantil", "Piscina aquecida coberta", "Sauna seca e a vapor", "Academia", "Salão de jogos", "Brinquedoteca", "Guarda-volumes náutico", "Lavanderia inteligente", "Concierge", "Portaria 24h"],
  "dna": ["Piscina no rooftop", "Piscinas externas", "Piscina infantil", "Piscina aquecida", "Hidromassagem", "Sauna seca e a vapor", "Cinema", "Academia", "Salão de jogos", "Brinquedoteca", "Espaço gourmet", "Recepção 24h"],
 },
 "all_photos": "Ver todas as fotos", "more": "+{n} fotos",
 "rv_eyebrow": "Avaliações", "rv_h2": "Hóspedes que <em>voltam</em> e recomendam",
 "rv_p": "Nossas notas vêm de avaliações reais de hóspedes no Airbnb. Elas mostram o cuidado com cada detalhe, da limpeza à recepção.",
 "aw_super": ("Anfitrião Superhost", "Mais de 1.000 hospedagens com avaliações excelentes, 100% de taxa de resposta e retorno em até 1 hora."),
 "aw_fav": ("Preferido dos hóspedes", "Selo do Airbnb para os anúncios mais amados pelos hóspedes, com base em avaliações e confiabilidade. O Bambu 202 está entre o top 1%."),
 "cats": ["Limpeza", "Exatidão", "Check-in", "Comunicação", "Localização", "Custo-benefício"],
 "read_reviews": "Ler as avaliações no Airbnb →",
 "topics_title": "Mais citados pelos hóspedes:",
 "topics": [("Hospitalidade", 26), ("Localização", 18), ("Limpeza", 16), ("Espaço interno", 12), ("Conforto", 9), ("Família", 9)],
 "mentions": "menções",
 "ig_eyebrow": "Instagram", "ig_h2": "Acompanhe a Bambu <em>no Instagram</em>", "ig_p": "Fotos dos apartamentos, novidades, dicas de Ubatuba e datas disponíveis. Siga para ficar por dentro.", "ig_name": "Apartamentos Bambu e DNA Resort", "ig_follow": "Seguir no Instagram", "ig_tile": "Ver no Instagram",
 "bk_eyebrow": "Como reservar", "bk_h2": "Reservar é <em>simples</em>",
 "steps": [("Escolha", "Veja as fotos e escolha o apartamento ideal para a sua viagem."), ("Chame no WhatsApp", "Envie as datas e o número de hóspedes. Respondemos rapidinho."), ("Confirme", "Combinamos valores e pagamento direto com o anfitrião. Se preferir, reserve pelo Airbnb.")],
 "loc_eyebrow": "Localização", "loc_h2": "Hospedagem na <em>Praia Grande</em>, Ubatuba",
 "loc_p": "A Praia Grande é uma das praias mais procuradas de Ubatuba e do Litoral Norte de SP: extensa, com mar para banho e surfe, quiosques, restaurantes e comércio na orla, e fácil acesso às praias vizinhas e ao Centro.",
 "open_maps": "Abrir no Maps", "loc_bambu": "Apartamentos 202 e 410 · Frente ao mar", "loc_dna": "Apartamento 14.4.1 · A ~100 m do mar",
 "near": ["Orla com quiosques e restaurantes", "Praias das Toninhas e Enseada por perto", "Centro de Ubatuba a poucos minutos", "Trilhas, ilhas e mais de 100 praias na região"],
 "map_title": "Mapa da Praia Grande, Ubatuba",
 "faq_eyebrow": "Dúvidas frequentes", "faq_h2": "Perguntas <em>frequentes</em>",
 "faq": [
  ("Como funciona a locação por temporada em Ubatuba?", "É só chamar no WhatsApp com as datas e o número de hóspedes. Confirmamos a disponibilidade e combinamos tudo diretamente. Se preferir, também é possível reservar pelo Airbnb."),
  ("Quantas pessoas cabem em cada apartamento?", "Até 6 hóspedes: suíte com cama queen, quarto com duas camas de solteiro e sofá-cama na sala."),
  ("Os apartamentos ficam perto da praia?", "Sim. Os apartamentos do Condomínio Bambu ficam de frente para a Praia Grande, com vista para o mar. O Reserva DNA fica a cerca de 100 metros da areia."),
  ("Tem ar-condicionado e Wi-Fi?", "Sim. Todos os apartamentos têm ar-condicionado em todos os quartos e Wi-Fi."),
  ("Roupa de cama e toalhas estão incluídas?", "Roupa de cama, toalhas e produtos de higiene e limpeza não estão inclusos. Fale com a gente pelo WhatsApp se tiver alguma dúvida."),
  ("Tem vaga de garagem?", "Sim. Os apartamentos do Bambu têm 1 vaga e o Reserva DNA tem 2 vagas. Veículos muito grandes, como picapes Dodge RAM, não cabem."),
  ("Posso levar meu pet?", "No Reserva DNA não são permitidos animais. Para os apartamentos do Condomínio Bambu, consulte a gente pelo WhatsApp."),
  ("Onde ficar em Ubatuba?", "A Praia Grande é uma das melhores regiões para se hospedar em Ubatuba: fica perto do Centro, tem orla com quiosques, restaurantes e comércio, e dá acesso fácil a praias como Toninhas e Enseada. Nossos apartamentos ficam de frente para o mar ou a poucos metros dele."),
 ],
 "fn_eyebrow": "Sua temporada começa aqui", "fn_h2": "Vamos planejar a sua viagem a Ubatuba?",
 "fn_p": "As melhores datas esgotam rápido, principalmente na alta temporada e nos feriados. Chame a gente e garanta o seu apartamento.",
 "follow": "Seguir @bambu.ubatuba",
 "ft_about": "Locação por temporada de apartamentos de alto padrão na Praia Grande, Ubatuba – SP. Anfitrião Superhost no Airbnb.",
 "ft_apts": "Apartamentos", "ft_contact": "Contato", "ft_links": "Navegação", "rights": "Todos os direitos reservados.",
 "lb_close": "Fechar galeria", "lb_prev": "Foto anterior", "lb_next": "Próxima foto",
 "photo_of": "Foto do apartamento",
},
"en": {
 "title": "Ubatuba Beachfront Vacation Rentals | Bambu",
 "desc": "Vacation rentals in Ubatuba, Brazil: high-end ocean-view apartments in Praia Grande, in resort-style buildings with infinity pools. Airbnb Superhost with 1,000+ stays. Book on WhatsApp.",
 "skip": "Skip to content",
 "nav": ["Apartments", "Amenities", "Reviews", "Location", "FAQ"],
 "menu": "Open menu", "wa_short": "WhatsApp", "wa_btn": "Book on WhatsApp",
 "wa_msg": "Hi! I saw the Bambu Ubatuba website and would like to check availability.",
 "wa_apt": "Hi! I'm interested in the {apt} apartment. I'd like to check availability for these dates: ",
 "eyebrow": "Praia Grande · Ubatuba · Brazil",
 "h1": "Beachfront <em>apartments</em> in Ubatuba",
 "lead": "High-end vacation rentals in Praia Grande, on the north coast of São Paulo, Brazil.<br>Brand-new, decorated ocean-view apartments in buildings with full leisure amenities: infinity pool, heated pool, sauna and gym.",
 "see_apts": "See apartments",
 "chip_rating": "5.0 on Airbnb", "chip_super": "Superhost", "chip_fav": "Guest favorite",
 "trust": [("1,000+", "stays hosted"), ("Superhost", "recognized Airbnb host"), ("Top 1%", "Guest favorite on Airbnb"), ("1 hour", "average response time")],
 "apts_eyebrow": "The apartments", "apts_h2": "Vacation apartments <em>in Ubatuba</em>",
 "apts_p": "Vacation rentals booked directly with the host. Apartments that sleep up to 6 guests, with an en-suite bedroom, air conditioning in every room, a gourmet balcony and a parking space.",
 "condo": {"bambu": "Bambu Building · Ocean view", "dna": "Reserva DNA Resort · Beachfront"},
 "reviews_word": "reviews", "see_airbnb": "View on Airbnb", "photos": "See all {n} photos",
 "fav_badge": "Guest favorite", "top1": "Top 1% on Airbnb",
 "spec": {"suites": "suites", "social": "+ 1 half bath", "guests": "guests", "bedrooms": "bedrooms", "beds": "beds", "baths": "bathrooms", "parking_1": "parking space", "parking_n": "parking spaces", "ac": "in every bedroom"},
 "ac": "A/C",
 "apt_desc": {
  "bambu-202": "A brand-new, fully decorated apartment facing the sea at Praia Grande. Gourmet balcony with a view, full kitchen, suite with a queen bed, bedroom with two single beds and a sofa bed in the living room.",
  "bambu-410": "On the 4th floor, with one of the best views in the building: ocean, mountains and the Praia Grande shoreline. Modern, complete and decorated, with a gourmet balcony, queen suite and a twin bedroom.",
  "reserva-dna": "A true beachfront resort.<br>Spacious and comfortable, with 2 suites, a gourmet balcony with barbecue grill overlooking the garden, a queen suite and 2 parking spaces.",
 },
 "apt_hl": {
  "bambu-202": ["Ocean view", "Gourmet balcony", "Infinity pool", "Wi-Fi"],
  "bambu-410": ["Ocean & mountain view", "Gourmet balcony", "Heated pool", "Wi-Fi"],
  "reserva-dna": ["Balcony barbecue grill", "2 suites", "Cinema & hot tub", "Wi-Fi"],
 },
 "lz_eyebrow": "Amenities", "lz_h2": "Resort-style living <em>by the beach</em>",
 "lz_p": "Both buildings offer amenities for all ages, so you can enjoy Ubatuba even on rainy days.",
 "condos": {
  "bambu": ("Bambu Building", "A new building facing Praia Grande, with a rooftop infinity pool overlooking the ocean. Home to apartments 202 and 410."),
  "dna": ("Reserva DNA Resort", "A beachfront resort with gardens, several pools, a rooftop and full family amenities. Home to apartment 14.4.1."),
 },
 "amen": {
  "bambu": ["Infinity pool", "Kids' pool", "Indoor heated pool", "Dry & steam sauna", "Gym", "Game room", "Kids' playroom", "Surf & beach gear storage", "Smart laundry", "Concierge", "24h front desk"],
  "dna": ["Rooftop pool", "Outdoor pools", "Kids' pool", "Heated pool", "Hot tub", "Dry & steam sauna", "Cinema", "Gym", "Game room", "Kids' playroom", "Gourmet area", "24h reception"],
 },
 "all_photos": "See all photos", "more": "+{n} photos",
 "rv_eyebrow": "Reviews", "rv_h2": "Guests who <em>come back</em> and recommend us",
 "rv_p": "Our scores come from real guest reviews on Airbnb. They reflect our care for every detail, from cleanliness to check-in.",
 "aw_super": ("Superhost", "1,000+ stays with outstanding reviews, a 100% response rate and replies within an hour."),
 "aw_fav": ("Guest favorite", "Airbnb's badge for the homes guests love most, based on ratings, reviews and reliability. Bambu 202 ranks in the top 1%."),
 "cats": ["Cleanliness", "Accuracy", "Check-in", "Communication", "Location", "Value"],
 "read_reviews": "Read the reviews on Airbnb →",
 "topics_title": "Most mentioned by guests:",
 "topics": [("Hospitality", 26), ("Location", 18), ("Cleanliness", 16), ("Indoor space", 12), ("Comfort", 9), ("Family", 9)],
 "mentions": "mentions",
 "ig_eyebrow": "Instagram", "ig_h2": "Follow Bambu <em>on Instagram</em>", "ig_p": "Apartment photos, news, Ubatuba tips and available dates. Follow along.", "ig_name": "Bambu & DNA Resort Apartments", "ig_follow": "Follow on Instagram", "ig_tile": "View on Instagram",
 "bk_eyebrow": "How to book", "bk_h2": "Booking is <em>easy</em>",
 "steps": [("Choose", "Browse the photos and pick the right apartment for your trip."), ("Message us on WhatsApp", "Send your dates and number of guests. We reply fast."), ("Confirm", "Agree on price and payment directly with the host, or book on Airbnb if you prefer.")],
 "loc_eyebrow": "Location", "loc_h2": "Where to stay: <em>Praia Grande</em>, Ubatuba",
 "loc_p": "Praia Grande is one of Ubatuba's most popular beaches: long, great for swimming and surfing, with kiosks, restaurants and shops along the waterfront and easy access to nearby beaches and downtown.",
 "open_maps": "Open in Maps", "loc_bambu": "Apartments 202 & 410 · Beachfront", "loc_dna": "Apartment 14.4.1 · ~100 m from the sea",
 "near": ["Waterfront kiosks and restaurants", "Toninhas and Enseada beaches nearby", "Downtown Ubatuba minutes away", "Trails, islands and 100+ beaches in the region"],
 "map_title": "Map of Praia Grande, Ubatuba",
 "faq_eyebrow": "FAQ", "faq_h2": "Frequently asked <em>questions</em>",
 "faq": [
  ("How do I book an apartment?", "Just message us on WhatsApp with your dates and number of guests. We'll confirm availability and arrange everything directly. You can also book through Airbnb."),
  ("How many people does each apartment sleep?", "Up to 6 guests: a suite with a queen bed, a bedroom with two single beds and a sofa bed in the living room."),
  ("Are the apartments close to the beach?", "Yes. The Bambu apartments face Praia Grande with an ocean view. Reserva DNA is about 100 meters from the sand."),
  ("Is there air conditioning and Wi-Fi?", "Yes. Every apartment has air conditioning in all bedrooms and Wi-Fi."),
  ("Are bed linens and towels included?", "Bed linens, towels, toiletries and cleaning supplies are not included. Message us on WhatsApp if you have any questions."),
  ("Is there parking?", "Yes. The Bambu apartments have 1 parking space and Reserva DNA has 2. Very large vehicles, such as Dodge RAM pickups, do not fit."),
  ("Can I bring my pet?", "Pets are not allowed at Reserva DNA. For the Bambu apartments, please ask us on WhatsApp."),
  ("Where should I stay in Ubatuba?", "Praia Grande is one of the best areas to stay in Ubatuba: close to downtown, with waterfront kiosks, restaurants and shops, and easy access to beaches such as Toninhas and Enseada. Our apartments face the sea or are just steps away."),
 ],
 "fn_eyebrow": "Your getaway starts here", "fn_h2": "Shall we plan your trip to Ubatuba?",
 "fn_p": "The best dates book up fast, especially in high season and on holidays. Message us and secure your apartment.",
 "follow": "Follow @bambu.ubatuba",
 "ft_about": "High-end vacation apartments in Praia Grande, Ubatuba – SP, Brazil. Airbnb Superhost.",
 "ft_apts": "Apartments", "ft_contact": "Contact", "ft_links": "Explore", "rights": "All rights reserved.",
 "lb_close": "Close gallery", "lb_prev": "Previous photo", "lb_next": "Next photo",
 "photo_of": "Apartment photo",
},
"es": {
 "title": "Alquiler Vacacional en Ubatuba Frente al Mar | Bambu",
 "desc": "Alquiler vacacional en Ubatuba, Brasil: apartamentos de alto nivel con vista al mar en Praia Grande, en edificios tipo resort con piscina infinita. Anfitrión Superhost con más de 1.000 estadías. Reserva por WhatsApp.",
 "skip": "Ir al contenido",
 "nav": ["Apartamentos", "Áreas comunes", "Reseñas", "Ubicación", "Preguntas"],
 "menu": "Abrir menú", "wa_short": "WhatsApp", "wa_btn": "Reservar por WhatsApp",
 "wa_msg": "¡Hola! Vi el sitio de Bambu Ubatuba y quisiera consultar disponibilidad.",
 "wa_apt": "¡Hola! Me interesa el apartamento {apt}. Quisiera consultar disponibilidad para las fechas: ",
 "eyebrow": "Praia Grande · Ubatuba · Brasil",
 "h1": "Apartamentos <em>frente al mar</em> en Ubatuba",
 "lead": "Alquiler vacacional de alto nivel en Praia Grande, litoral norte de São Paulo, Brasil.<br>Apartamentos nuevos y decorados, con vista al mar en edificios con estructura de ocio completa: piscina infinita, piscina climatizada, sauna y gimnasio.",
 "see_apts": "Ver apartamentos",
 "chip_rating": "5,0 en Airbnb", "chip_super": "Superhost", "chip_fav": "Favorito de los huéspedes",
 "trust": [("+1.000", "estadías realizadas"), ("Superhost", "anfitrión reconocido en Airbnb"), ("Top 1%", "Favorito de los huéspedes en Airbnb"), ("1 hora", "tiempo medio de respuesta")],
 "apts_eyebrow": "Los apartamentos", "apts_h2": "Apartamentos vacacionales <em>en Ubatuba</em>",
 "apts_p": "Alquiler vacacional directo con el anfitrión. Apartamentos para hasta 6 huéspedes, con suite, aire acondicionado en todos los ambientes, balcón gourmet y cochera.",
 "condo": {"bambu": "Edificio Bambu · Vista al mar", "dna": "Reserva DNA Resort · Frente al mar"},
 "reviews_word": "reseñas", "see_airbnb": "Ver en Airbnb", "photos": "Ver las {n} fotos",
 "fav_badge": "Favorito de los huéspedes", "top1": "Top 1% de Airbnb",
 "spec": {"suites": "suites", "social": "+ 1 de visitas", "guests": "huéspedes", "bedrooms": "dormitorios", "beds": "camas", "baths": "baños", "parking_1": "cochera", "parking_n": "cocheras", "ac": "en todos los dormitorios"},
 "ac": "Aire acond.",
 "apt_desc": {
  "bambu-202": "Apartamento nuevo y totalmente decorado frente al mar de Praia Grande. Balcón gourmet con vista, cocina completa, suite con cama queen, dormitorio con dos camas individuales y sofá cama en la sala.",
  "bambu-410": "En el 4.º piso, con una de las vistas más lindas del edificio: mar, montañas y la costanera de Praia Grande. Moderno, completo y decorado, con balcón gourmet, suite queen y dormitorio con dos camas.",
  "reserva-dna": "Un verdadero resort junto al mar.<br>Amplio y cómodo, con 2 suites, balcón gourmet con parrilla y vista al jardín, suite con cama queen y 2 cocheras.",
 },
 "apt_hl": {
  "bambu-202": ["Vista al mar", "Balcón gourmet", "Piscina infinita", "Wi-Fi"],
  "bambu-410": ["Vista al mar y montañas", "Balcón gourmet", "Piscina climatizada", "Wi-Fi"],
  "reserva-dna": ["Parrilla en el balcón", "2 suites", "Cine y jacuzzi", "Wi-Fi"],
 },
 "lz_eyebrow": "Áreas comunes", "lz_h2": "Estructura de <em>resort</em> junto al mar",
 "lz_p": "Los dos edificios ofrecen ocio para todas las edades, para disfrutar Ubatuba incluso en días de lluvia.",
 "condos": {
  "bambu": ("Edificio Bambu", "Edificio nuevo frente a Praia Grande, con rooftop y piscina infinita mirando al mar. Aquí están los apartamentos 202 y 410."),
  "dna": ("Reserva DNA Resort", "Resort frente al mar con jardines, varias piscinas, rooftop y ocio completo para la familia. Aquí está el apartamento 14.4.1."),
 },
 "amen": {
  "bambu": ["Piscina infinita", "Piscina infantil", "Piscina climatizada cubierta", "Sauna seca y de vapor", "Gimnasio", "Sala de juegos", "Sala infantil", "Guardería náutica", "Lavandería inteligente", "Conserjería", "Portería 24 h"],
  "dna": ["Piscina en el rooftop", "Piscinas exteriores", "Piscina infantil", "Piscina climatizada", "Jacuzzi", "Sauna seca y de vapor", "Cine", "Gimnasio", "Sala de juegos", "Sala infantil", "Espacio gourmet", "Recepción 24 h"],
 },
 "all_photos": "Ver todas las fotos", "more": "+{n} fotos",
 "rv_eyebrow": "Reseñas", "rv_h2": "Huéspedes que <em>vuelven</em> y nos recomiendan",
 "rv_p": "Nuestras calificaciones provienen de reseñas reales de huéspedes en Airbnb. Reflejan el cuidado en cada detalle, de la limpieza a la llegada.",
 "aw_super": ("Anfitrión Superhost", "Más de 1.000 estadías con reseñas excelentes, 100% de tasa de respuesta y respuesta en menos de 1 hora."),
 "aw_fav": ("Favorito de los huéspedes", "Distintivo de Airbnb para los alojamientos más queridos, según calificaciones, reseñas y confiabilidad. Bambu 202 está en el top 1%."),
 "cats": ["Limpieza", "Veracidad", "Llegada", "Comunicación", "Ubicación", "Calidad-precio"],
 "read_reviews": "Leer las reseñas en Airbnb →",
 "topics_title": "Lo más mencionado por los huéspedes:",
 "topics": [("Hospitalidad", 26), ("Ubicación", 18), ("Limpieza", 16), ("Espacio interior", 12), ("Comodidad", 9), ("Familia", 9)],
 "mentions": "menciones",
 "ig_eyebrow": "Instagram", "ig_h2": "Sigue a Bambu <em>en Instagram</em>", "ig_p": "Fotos de los apartamentos, novedades, consejos de Ubatuba y fechas disponibles. Síguenos.", "ig_name": "Apartamentos Bambu y DNA Resort", "ig_follow": "Seguir en Instagram", "ig_tile": "Ver en Instagram",
 "bk_eyebrow": "Cómo reservar", "bk_h2": "Reservar es <em>simple</em>",
 "steps": [("Elige", "Mira las fotos y elige el apartamento ideal para tu viaje."), ("Escríbenos por WhatsApp", "Envía las fechas y la cantidad de huéspedes. Respondemos rápido."), ("Confirma", "Acordamos precio y pago directamente con el anfitrión. Si prefieres, reserva por Airbnb.")],
 "loc_eyebrow": "Ubicación", "loc_h2": "Dónde alojarse: <em>Praia Grande</em>, Ubatuba",
 "loc_p": "Praia Grande es una de las playas más buscadas de Ubatuba: extensa, ideal para bañarse y surfear, con quioscos, restaurantes y comercios en la costanera y fácil acceso a playas vecinas y al Centro.",
 "open_maps": "Abrir en Maps", "loc_bambu": "Apartamentos 202 y 410 · Frente al mar", "loc_dna": "Apartamento 14.4.1 · A ~100 m del mar",
 "near": ["Costanera con quioscos y restaurantes", "Playas Toninhas y Enseada cerca", "Centro de Ubatuba a pocos minutos", "Senderos, islas y más de 100 playas en la región"],
 "map_title": "Mapa de Praia Grande, Ubatuba",
 "faq_eyebrow": "Preguntas frecuentes", "faq_h2": "Preguntas <em>frecuentes</em>",
 "faq": [
  ("¿Cómo reservo un apartamento?", "Escríbenos por WhatsApp con las fechas y la cantidad de huéspedes. Confirmamos la disponibilidad y coordinamos todo directamente. También puedes reservar por Airbnb."),
  ("¿Cuántas personas caben en cada apartamento?", "Hasta 6 huéspedes: suite con cama queen, dormitorio con dos camas individuales y sofá cama en la sala."),
  ("¿Los apartamentos están cerca de la playa?", "Sí. Los apartamentos del edificio Bambu están frente a Praia Grande, con vista al mar. Reserva DNA está a unos 100 metros de la arena."),
  ("¿Tienen aire acondicionado y Wi-Fi?", "Sí. Todos los apartamentos tienen aire acondicionado en todos los dormitorios y Wi-Fi."),
  ("¿Incluyen ropa de cama y toallas?", "No se incluyen ropa de cama, toallas ni productos de higiene y limpieza. Escríbenos por WhatsApp si tienes dudas."),
  ("¿Hay cochera?", "Sí. Los apartamentos Bambu tienen 1 cochera y Reserva DNA tiene 2. Vehículos muy grandes, como camionetas Dodge RAM, no caben."),
  ("¿Puedo llevar mi mascota?", "En Reserva DNA no se permiten mascotas. Para los apartamentos del edificio Bambu, consúltanos por WhatsApp."),
  ("¿Dónde alojarse en Ubatuba?", "Praia Grande es una de las mejores zonas para alojarse en Ubatuba: cerca del Centro, con quioscos, restaurantes y comercios en la costanera y fácil acceso a playas como Toninhas y Enseada. Nuestros apartamentos están frente al mar o a pocos pasos."),
 ],
 "fn_eyebrow": "Tus vacaciones empiezan aquí", "fn_h2": "¿Planeamos tu viaje a Ubatuba?",
 "fn_p": "Las mejores fechas se agotan rápido, sobre todo en temporada alta y feriados. Escríbenos y asegura tu apartamento.",
 "follow": "Seguir @bambu.ubatuba",
 "ft_about": "Apartamentos de alto nivel para vacaciones en Praia Grande, Ubatuba – SP, Brasil. Anfitrión Superhost en Airbnb.",
 "ft_apts": "Apartamentos", "ft_contact": "Contacto", "ft_links": "Navegación", "rights": "Todos los derechos reservados.",
 "lb_close": "Cerrar galería", "lb_prev": "Foto anterior", "lb_next": "Foto siguiente",
 "photo_of": "Foto del apartamento",
},
}

LABELS = {
 "balcony_sea": ("Varanda gourmet com vista para o mar", "Gourmet balcony with ocean view", "Balcón gourmet con vista al mar"),
 "sea_view": ("Vista para o mar da Praia Grande", "Ocean view over Praia Grande", "Vista al mar de Praia Grande"),
 "living": ("Sala de estar integrada", "Open-plan living room", "Sala de estar integrada"),
 "kitchen": ("Cozinha equipada", "Fully equipped kitchen", "Cocina equipada"),
 "balcony": ("Varanda gourmet", "Gourmet balcony", "Balcón gourmet"),
 "balcony_bbq": ("Varanda gourmet com churrasqueira", "Balcony with barbecue grill", "Balcón gourmet con parrilla"),
 "suite": ("Suíte com cama queen", "Suite with queen bed", "Suite con cama queen"),
 "bedroom": ("Quarto com duas camas de solteiro", "Bedroom with two single beds", "Dormitorio con dos camas individuales"),
 "bathroom": ("Banheiro", "Bathroom", "Baño"),
 "infinity_pool": ("Piscina de borda infinita com vista para o mar", "Infinity pool with ocean view", "Piscina infinita con vista al mar"),
 "deck": ("Deck com espreguiçadeiras e vista para o mar", "Sun deck with ocean view", "Solárium con vista al mar"),
 "heated_pool": ("Piscina aquecida coberta", "Indoor heated pool", "Piscina climatizada cubierta"),
 "garden": ("Jardim com pergolado", "Garden with pergola", "Jardín con pérgola"),
 "facade": ("Fachada do condomínio", "Building façade", "Fachada del edificio"),
 "lobby": ("Recepção e lobby", "Reception and lobby", "Recepción y lobby"),
 "game_room": ("Salão de jogos", "Game room", "Sala de juegos"),
 "playroom": ("Brinquedoteca", "Kids' playroom", "Sala infantil"),
 "gym": ("Academia", "Gym", "Gimnasio"),
 "sauna": ("Sauna", "Sauna", "Sauna"),
 "laundry": ("Lavanderia", "Laundry room", "Lavandería"),
 "aerial": ("Vista aérea do resort frente ao mar", "Aerial view of the beachfront resort", "Vista aérea del resort frente al mar"),
 "pool": ("Piscina do resort", "Resort pool", "Piscina del resort"),
 "beach_view": ("Vista da Praia Grande", "View of Praia Grande beach", "Vista de Praia Grande"),
 "pergola": ("Pergolado à beira da piscina", "Poolside pergola", "Pérgola junto a la piscina"),
 "hot_tub": ("Hidromassagem", "Hot tub", "Jacuzzi"),
 "gourmet": ("Espaço gourmet", "Gourmet area", "Espacio gourmet"),
}

# ------------------------------ Ícones ------------------------------
def ic(body, vb="0 0 24 24", fill=False):
    a = 'fill="currentColor"' if fill else 'fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"'
    return f'<svg viewBox="{vb}" {a} aria-hidden="true">{body}</svg>'

WA = ic('<path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.8 11.9 11.9 0 0 0 4.6 4c1.7.7 2.4.8 3.2.7.5-.1 1.5-.6 1.8-1.2.2-.6.2-1.1.1-1.2l-.4-.3Z"/>', fill=True)
STAR = ic('<path d="m12 2.5 2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 17.4l-5.9 3.1 1.2-6.5L2.5 9.4l6.6-.9L12 2.5Z"/>', fill=True)
IG = ic('<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r=".6" fill="currentColor"/>')
PIN = ic('<path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21Z"/><circle cx="12" cy="9.5" r="2.5"/>')
CAM = ic('<path d="M4 8h3l2-3h6l2 3h3v11H4z"/><circle cx="12" cy="13" r="3.5"/>')
ARROW = ic('<path d="M5 12h14M13 6l6 6-6 6"/>')
CLOSE = ic('<path d="M6 6l12 12M18 6 6 18"/>')
PREV = ic('<path d="m15 5-7 7 7 7"/>')
NEXT = ic('<path d="m9 5 7 7-7 7"/>')
AIRBNB = ic('<path d="M12 3c-1.3 0-2 .9-2.8 2.6L4 16.7c-1 2.3.6 4.3 2.6 4.3 1.6 0 3.2-1.3 5.4-3.9 2.2 2.6 3.8 3.9 5.4 3.9 2 0 3.6-2 2.6-4.3L14.8 5.6C14 3.9 13.3 3 12 3Zm0 12.6c-1.5-1.9-2.4-3.5-2.4-4.7a2.4 2.4 0 1 1 4.8 0c0 1.2-.9 2.8-2.4 4.7Z"/>')
I_GUESTS = ic('<circle cx="9" cy="8" r="3.2"/><path d="M3 19c.6-3.3 3-5 6-5s5.4 1.7 6 5"/><circle cx="17" cy="9" r="2.4"/><path d="M16.5 14c2.6.2 4 1.8 4.5 4.5"/>')
I_BED = ic('<path d="M3 18v-7a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v7M3 15h18M6 9V6h5v3M13 9V6h5v3"/>')
I_DOOR = ic('<path d="M5 21V4h11v17M3 21h18M13 12.5v.5"/>')
I_BATH = ic('<path d="M4 12h16v3a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5v-3ZM6 12V5.5A2.5 2.5 0 0 1 10.5 4M7 20l-1 2M17 20l1 2"/>')
I_CAR = ic('<path d="M5 16V11l2-5h10l2 5v5M3 16h18v3H3zM7 16v3M17 16v3M5 11h14"/>')
I_AC = ic('<rect x="3" y="5" width="18" height="7" rx="2"/><path d="M7 15c0 1.5-1 2-1 3M12 15v4M17 15c0 1.5 1 2 1 3"/>')
I_HOME = ic('<path d="M3 11 12 4l9 7M5 10v10h14V10"/>')
I_MEDAL = ic('<circle cx="12" cy="14" r="6"/><path d="m8.5 3 3.5 5 3.5-5M12 11l1 2 2.2.3-1.6 1.5.4 2.2-2-1-2 1 .4-2.2-1.6-1.5L11 13z"/>')
I_CLOCK = ic('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>')

def _leaves(cx, cy, r, rx, ry, n=7, a0=105, a1=235):
    """Folhas ao longo de dois arcos espelhados (coroa de louros genérica)."""
    out = []
    for k in range(n):
        th = a0 + (a1 - a0) * k / (n - 1)
        for ang in (th, 180 - th):
            x = cx + r * math.cos(math.radians(ang)); y = cy + r * math.sin(math.radians(ang))
            tilt = 22 if ang == th else -22
            out.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{rx}" ry="{ry}" transform="rotate({ang + tilt:.0f} {x:.1f} {y:.1f})"/>')
    return "".join(out)

def laurel(size=24, color="currentColor"):
    return (f'<svg viewBox="0 0 64 64" width="{size}" height="{size}" fill="{color}" aria-hidden="true">'
            + _leaves(32, 33, 21, 4.6, 9.5, 5, 115, 235) + '</svg>')

def wreath(cls="big"):
    return (f'<svg class="{cls}" viewBox="0 0 100 100" fill="currentColor" aria-hidden="true">' + _leaves(50, 50, 38, 4.6, 10.5, 7) +
            '<text x="50" y="60" text-anchor="middle" font-family="Cormorant,Georgia,serif" font-size="30" font-weight="600">5,0</text></svg>')

LOGO = ('<svg viewBox="0 0 40 40" aria-hidden="true"><defs><linearGradient id="lg" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="#16849a"/><stop offset="1" stop-color="#2f7a55"/></linearGradient></defs>'
        '<circle cx="20" cy="20" r="19" fill="url(#lg)"/>'
        '<path d="M15 31V9M15 15.5h-1.6M15 22h-1.6M15 28h-1.6" stroke="#fff" stroke-width="2.2" stroke-linecap="round"/>'
        '<path d="M16 14c3-4.5 8-5.5 12-4.5-2.5 3.6-6.6 5.2-12 4.5Z" fill="#cfeedd"/>'
        '<path d="M16 21c3.4-3 8-3.2 11.5-1.6-3 2.8-7 3.4-11.5 1.6Z" fill="#fff"/>'
        '<path d="M22 31V17" stroke="#fff" stroke-width="1.8" stroke-linecap="round" opacity=".75"/></svg>')

def stripes_us():
    s = ['<rect width="38" height="20" fill="#B22234"/>']
    h = 20 / 13
    for k in range(1, 13, 2):
        s.append(f'<rect y="{k*h:.3f}" width="38" height="{h:.3f}" fill="#fff"/>')
    s.append(f'<rect width="15.2" height="{7*h:.3f}" fill="#3C3B6E"/>')
    for r in range(4):
        for c in range(5):
            s.append(f'<circle cx="{1.6+c*3:.1f}" cy="{1.5+r*2.5:.1f}" r=".55" fill="#fff"/>')
    return '<svg viewBox="0 0 38 20" preserveAspectRatio="none" aria-hidden="true">' + "".join(s) + "</svg>"

FLAGS = {
 "pt": ('<svg viewBox="0 0 30 21" preserveAspectRatio="none" aria-hidden="true"><rect width="30" height="21" fill="#009c3b"/>'
        '<path d="M15 2.4 27.4 10.5 15 18.6 2.6 10.5Z" fill="#ffdf00"/><circle cx="15" cy="10.5" r="4.9" fill="#002776"/>'
        '<path d="M10.3 9.4c3.2-.6 6.5 0 9.4 1.7" stroke="#fff" stroke-width=".8" fill="none"/></svg>', "Português (Brasil)"),
 "en": (stripes_us(), "English"),
 "es": ('<svg viewBox="0 0 30 20" preserveAspectRatio="none" aria-hidden="true"><rect width="30" height="20" fill="#c60b1e"/>'
        '<rect y="5" width="30" height="10" fill="#ffc400"/></svg>', "Español"),
}

# ------------------------------ Utilidades ------------------------------
def strip_tags(x):
    import re
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", x)).strip()

def num(v, lang, dec=2):
    s = f"{v:.{dec}f}".rstrip("0").rstrip(".") if dec else str(v)
    if "." not in s and dec:
        s = f"{v:.1f}"
    return s.replace(".", ",") if lang != "en" else s

def wa_link(text):
    return f"https://wa.me/{WHATSAPP}?text={quote(text)}"

def img_tag(it, P, alt, sizes, lazy=True, cls=""):
    return (f'<img src="{P}{it["thumb"]}" width="{it["tw"]}" height="{it["th"]}" alt="{escape(alt)}"'
            + (' loading="lazy" decoding="async"' if lazy else "") + (f' class="{cls}"' if cls else "") + f' sizes="{sizes}">')

def alt_for(it, lang, title):
    return f'{LABELS[it["label"]][LANGS.index(lang)]} – {title}, Ubatuba'

# ------------------------------ Página ------------------------------
def build(lang, images, css):
    t = T[lang]; P = PREFIX[lang]; L = LANGS.index(lang)
    url = SITE_URL + PATH[lang]
    ids = ["apartamentos", "lazer", "avaliacoes", "localizacao", "duvidas"]
    titles = {a["key"]: f'{"Apartamento " if lang != "en" else ""}{a["name"]}{" apartment" if lang == "en" else ""}' for a in APTS}
    titles["lazer-bambu"] = t["condos"]["bambu"][0]
    titles["lazer-dna"] = t["condos"]["dna"][0]

    albums = {k: {"title": titles[k], "items": [{"src": P + it["src"], "w": it["w"], "h": it["h"], "alt": alt_for(it, lang, titles[k])} for it in v]}
              for k, v in images.items()}

    # --- Head ---
    alt_links = "".join(f'<link rel="alternate" hreflang="{HREFLANG[l]}" href="{SITE_URL}{PATH[l]}">' for l in LANGS)
    alt_links += f'<link rel="alternate" hreflang="x-default" href="{SITE_URL}/">'
    hero = f"{P}img/hero/bambu-ubatuba-vista-mar"
    og_img = f"{SITE_URL}/img/hero/og-bambu-ubatuba.jpg"

    schema = [
        {"@context": "https://schema.org", "@type": "LodgingBusiness", "@id": SITE_URL + "/#business",
         "name": "Bambu Ubatuba", "url": url, "description": t["desc"], "image": og_img,
         "telephone": "+" + WHATSAPP, "priceRange": "$$$",
         "address": {"@type": "PostalAddress", "addressLocality": "Ubatuba", "addressRegion": "SP", "addressCountry": "BR"},
         "areaServed": "Ubatuba, SP", "sameAs": [INSTAGRAM] + [a["airbnb"] for a in APTS],
         "amenityFeature": [{"@type": "LocationFeatureSpecification", "name": n, "value": True} for n in t["amen"]["bambu"][:6]],
         "containsPlace": [
             {"@type": "Apartment", "name": titles[a["key"]], "url": a["airbnb"], "description": strip_tags(t["apt_desc"][a["key"]]),
              "image": [SITE_URL + "/" + it["src"] for it in images[a["key"]][:8]],
              "numberOfRooms": a["bedrooms"], "numberOfBedrooms": a["bedrooms"], "numberOfBathroomsTotal": a["baths"] + a.get("social", 0),
              "occupancy": {"@type": "QuantitativeValue", "maxValue": a["guests"]},
              "petsAllowed": False if a["condo"] == "dna" else None,
              "aggregateRating": {"@type": "AggregateRating", "ratingValue": a["rating"], "reviewCount": a["reviews"], "bestRating": 5}}
             for a in APTS],
         "inLanguage": HREFLANG[lang]},
        {"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": HREFLANG[lang],
         "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": r}} for q, r in t["faq"]]},
        {"@context": "https://schema.org", "@type": "WebSite", "name": "Bambu Ubatuba", "url": SITE_URL + "/", "inLanguage": HREFLANG[lang]},
    ]
    for s in schema[0]["containsPlace"]:
        if s["petsAllowed"] is None:
            del s["petsAllowed"]

    head = f'''<!doctype html>
<html lang="{HREFLANG[lang]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{escape(t["title"])}</title>
<meta name="description" content="{escape(t["desc"])}">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{url}">
{alt_links}
<meta name="theme-color" content="#062c42">
<meta name="geo.region" content="BR-SP"><meta name="geo.placename" content="Ubatuba">
<meta property="og:type" content="website"><meta property="og:site_name" content="Bambu Ubatuba">
<meta property="og:title" content="{escape(t["title"])}"><meta property="og:description" content="{escape(t["desc"])}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{og_img}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:locale" content="{OG_LOCALE[lang]}">{"".join(f'<meta property="og:locale:alternate" content="{OG_LOCALE[l]}">' for l in LANGS if l != lang)}
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{P}favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{P}apple-touch-icon.png">
<link rel="manifest" href="{P}site.webmanifest">
<link rel="preload" href="{P}fonts/cormorant.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{P}fonts/manrope.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" as="image" href="{hero}-wide.webp" media="(min-aspect-ratio: 1/1)" fetchpriority="high">
<link rel="preload" as="image" imagesrcset="{hero}-640.webp 640w, {hero}-960.webp 960w, {hero}-1200.webp 1200w" imagesizes="100vw" media="(max-aspect-ratio: 1/1)" fetchpriority="high">
<style>{css.replace("FONTS/", P + "fonts/")}</style>
<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False, separators=(",", ":"))}</script>
</head>'''

    # --- Header ---
    nav = "".join(f'<a href="#{i}">{n}</a>' for i, n in zip(ids, t["nav"]))
    langs = "".join(
        f'<a href="{PREFIX[lang]}{"" if l == "pt" else l + "/"}" hreflang="{HREFLANG[l]}" lang="{HREFLANG[l]}" title="{FLAGS[l][1]}" aria-label="{FLAGS[l][1]}"'
        + (' aria-current="true"' if l == lang else "") + f'>{FLAGS[l][0]}</a>'
        for l in LANGS)
    # links de idioma: a partir de /en/ o "pt" deve voltar para ../
    langs = langs.replace(f'href="{PREFIX[lang]}"', f'href="{PREFIX[lang] or "./"}"')
    header = f'''<a class="skip" href="#main">{t["skip"]}</a>
<header class="hdr"><div class="wrap hdr-in">
<a class="logo" href="#top" aria-label="Bambu Ubatuba"><img class="logo-w" src="{P}img/brand/logo-bambu-branco.svg" width="98" height="35" alt="Bambu Ubatuba"><img class="logo-c" src="{P}img/brand/logo-bambu.svg" width="98" height="35" alt=""></a>
<nav class="nav" aria-label="Menu">{nav}<a class="nav-ig" href="{INSTAGRAM}" target="_blank" rel="noopener"><img src="{P}img/brand/instagram-branco.png" width="17" height="17" alt="">Instagram</a></nav>
<div class="langs">{langs}</div>
<a class="hdr-ig" href="{INSTAGRAM}" target="_blank" rel="noopener" aria-label="Instagram @bambu.ubatuba"><img src="{P}img/brand/instagram-branco.png" width="26" height="26" alt=""></a>
<a class="btn btn-wa" href="{wa_link(t["wa_msg"])}" target="_blank" rel="noopener" aria-label="{t["wa_btn"]}">{WA}<span>{t["wa_short"]}</span></a>
<button class="burger" aria-label="{t["menu"]}" aria-expanded="false"><span></span><span></span><span></span></button>
</div></header>'''

    # --- Hero ---
    hero_html = f'''<section class="hero" id="top">
<picture>
<source media="(min-aspect-ratio: 1/1)" srcset="{hero}-wide.webp" width="1200" height="800">
<img src="{hero}-960.webp" srcset="{hero}-640.webp 640w, {hero}-960.webp 960w, {hero}-1200.webp 1200w" sizes="100vw" width="1200" height="1600" alt="{escape(LABELS["infinity_pool"][L])} – Bambu Ubatuba, Praia Grande" fetchpriority="high">
</picture>
<div class="wrap hero-in">
<span class="eyebrow">{t["eyebrow"]}</span>
<h1>{t["h1"]}</h1>
<p class="lead">{t["lead"]}</p>
<div class="hero-cta"><a class="btn btn-wa" href="{wa_link(t["wa_msg"])}" target="_blank" rel="noopener">{WA}{t["wa_btn"]}</a><a class="btn btn-light" href="#apartamentos">{t["see_apts"]}</a></div>
<ul class="chips">
<li class="chip">{STAR.replace('aria-hidden', 'style="color:#f3d68b" aria-hidden')}{t["chip_rating"]}</li>
<li class="chip">{I_MEDAL}{t["chip_super"]}</li>
<li class="chip">{laurel(20)}{t["chip_fav"]}</li>
</ul>
</div></section>'''

    trust_icons = [I_HOME, I_MEDAL, laurel(26), I_CLOCK]
    trust = '<section class="trust" aria-label="Destaques"><div class="wrap"><ul>' + "".join(
        f'<li class="rv"><span class="ic">{ico}</span><div><strong>{a}</strong><span>{b}</span></div></li>'
        for ico, (a, b) in zip(trust_icons, t["trust"])) + "</ul></div></section>"

    # --- Apartamentos ---
    sp = t["spec"]
    apts_html = []
    for a in APTS:
        k = a["key"]; imgs = images[k]; title = titles[k]
        cover = imgs[0]
        fav = (f'<span class="apt-fav">{laurel(18, "#1f5e40")}{t["fav_badge"]}{" · Top 1%" if a["top1"] else ""}</span>' if a["fav"] else "")
        specs = [
            (I_GUESTS, a["guests"], sp["guests"]), (I_DOOR, a["bedrooms"], sp["suites"] if a.get("suites") else sp["bedrooms"]),
            (I_BATH, a["baths"], sp["baths"] + (" " + sp["social"] if a.get("social") else "")), (I_CAR, a["parking"], sp["parking_1"] if a["parking"] == 1 else sp["parking_n"]),
        ]
        specs_html = "".join(f'<li>{i}<span><b>{v}</b> {l}</span></li>' for i, v, l in specs)
        hl = "".join(f"<li>{h}</li>" for h in t["apt_hl"][k][:3])
        thumbs = "".join(
            f'<button type="button" data-album="{k}" data-i="{n}" aria-label="{escape(alt_for(imgs[n], lang, title))}">'
            + img_tag(imgs[n], P, "", "120px") + "</button>" for n in (1, 2, 3))
        apts_html.append(f'''<article class="apt rv" id="{k}">
<div class="apt-cover">
<button type="button" class="apt-img" data-album="{k}" data-i="0" aria-label="{escape(t["photos"].format(n=len(imgs)))} – {escape(title)}">{img_tag(cover, P, alt_for(cover, lang, title), "(max-width:1080px) 84vw, 400px")}</button>
<div class="apt-top">{fav}<span class="apt-rate">{STAR}<b>{num(a["rating"], lang)}</b><span class="n">· {a["reviews"]}</span></span></div>
<div class="apt-cap"><span class="tag">{t["condo"][a["condo"]]}</span><h3>{a["name"]}</h3></div>
</div>
<div class="apt-body">
<ul class="specs">{specs_html}</ul>
<p class="apt-desc">{t["apt_desc"][k]}</p>
<ul class="hl">{hl}</ul>
<div class="apt-thumbs">{thumbs}<button type="button" class="apt-all" data-album="{k}">{CAM}<span>{t["photos"].format(n=len(imgs))}</span></button></div>
<div class="apt-cta"><a class="btn btn-wa" href="{wa_link(t["wa_apt"].format(apt=a["name"]))}" target="_blank" rel="noopener">{WA}{t["wa_btn"]}</a><a class="apt-link" href="{a["airbnb"]}" target="_blank" rel="noopener">{AIRBNB}{t["see_airbnb"]}</a></div>
</div></article>''')
    apts_sec = f'''<section class="sec" id="apartamentos"><div class="wrap">
<div class="sec-head center rv"><span class="eyebrow">{t["apts_eyebrow"]}</span><h2>{t["apts_h2"]}</h2><p>{t["apts_p"]}</p></div>
<div class="apts">{"".join(apts_html)}</div>
</div></section>'''

    # --- Lazer ---
    tabs, panels = [], []
    for n, (c, album) in enumerate((("bambu", "lazer-bambu"), ("dna", "lazer-dna"))):
        name, desc = t["condos"][c]; imgs = images[album]
        tabs.append(f'<button role="tab" id="tab-{c}" aria-controls="pn-{c}" aria-selected="{"true" if n == 0 else "false"}">{name}</button>')
        shown = 8
        cells = []
        for j in range(shown):
            extra = f'<span class="count">{t["more"].format(n=len(imgs) - shown)}</span>' if j == shown - 1 else ""
            cells.append(f'<button type="button" data-album="{album}" data-i="{j}" aria-label="{escape(alt_for(imgs[j], lang, name))}">'
                         + img_tag(imgs[j], P, alt_for(imgs[j], lang, name), "(max-width:860px) 50vw, 25vw") + extra + "</button>")
        amen = "".join(f"<li>{x}</li>" for x in t["amen"][c])
        panels.append(f'''<div class="panel" role="tabpanel" id="pn-{c}" aria-labelledby="tab-{c}"{" hidden" if n else ""}>
<div class="panel-top"><p>{desc}</p><button type="button" class="btn btn-light" data-album="{album}">{CAM}{t["all_photos"]}</button></div>
<ul class="amen">{amen}</ul>
<div class="bento">{"".join(cells)}</div></div>''')
    lazer_sec = f'''<section class="sec leisure" id="lazer"><div class="wrap">
<div class="sec-head rv"><span class="eyebrow">{t["lz_eyebrow"]}</span><h2>{t["lz_h2"]}</h2><p>{t["lz_p"]}</p></div>
<div class="tabs" role="tablist" aria-label="{t["lz_eyebrow"]}">{"".join(tabs)}</div>
{"".join(panels)}
</div></section>'''

    # --- Avaliações ---
    scores = []
    for a in APTS:
        bars = "".join(f'<li>{c}<i style="--v:{v/5*100:.0f}%"></i><b>{num(v, lang, 1)}</b></li>' for c, v in zip(t["cats"], a["cats"]))
        fav = f'<span class="fav">{laurel(16)}{t["top1"] if a["top1"] else t["fav_badge"]}</span>' if a["fav"] else ""
        scores.append(f'''<article class="score rv"><header><div><h3>{a["name"]}</h3></div><span class="big">{num(a["rating"], lang)}</span></header>
<p class="sub">{a["reviews"]} {t["reviews_word"]} · Airbnb</p><ul class="bars">{bars}</ul>
<div style="display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap">{fav}<a href="{a["airbnb"]}/reviews" target="_blank" rel="noopener">{t["read_reviews"]}</a></div></article>''')
    quotes = ""
    if REVIEWS:
        quotes = '<div class="quotes">' + "".join(
            f'<figure class="quote rv"><div class="stars">{STAR * 5}</div><blockquote>“{escape(r["text"].get(lang) or r["text"]["pt"])}”</blockquote>'
            f'<figcaption><b>{escape(r["name"])}</b>{escape(r.get("from", ""))} · {escape(r.get("date", ""))} · {escape(r.get("apt", ""))}</figcaption></figure>'
            for r in REVIEWS) + "</div>"
    topics = "".join(f'<span><b>{n}</b> · {c} {t["mentions"]}</span>' for n, c in t["topics"])
    rev_sec = f'''<section class="sec reviews" id="avaliacoes"><div class="wrap">
<div class="sec-head center rv"><span class="eyebrow">{t["rv_eyebrow"]}</span><h2>{t["rv_h2"]}</h2><p>{t["rv_p"]}</p></div>
<div class="rev-top">
<div class="award dark rv">{I_MEDAL.replace('<svg', '<svg class="big"')}<div><h3>{t["aw_super"][0]}</h3><p>{t["aw_super"][1]}</p></div></div>
<div class="award rv" style="color:var(--ink)">{wreath().replace("5,0", num(5.0, lang)).replace('fill="currentColor"', 'fill="#2f7a55"', 1)}<div><h3>{t["aw_fav"][0]}</h3><p>{t["aw_fav"][1]}</p></div></div>
</div>
<div class="scores">{"".join(scores)}</div>
{quotes}
<div class="topics rv" aria-label="{t["topics_title"]}">{topics}</div>
</div></section>'''

    # --- Instagram ---
    ig_png = f'{P}img/brand/instagram-branco.png'
    picks = [("lazer-bambu", 0), ("bambu-410", 0), ("lazer-dna", 0), ("bambu-202", 1), ("reserva-dna", 0), ("lazer-bambu", 1)]
    tiles = "".join(
        f'<a class="ig-tile" href="{INSTAGRAM}" target="_blank" rel="noopener" aria-label="{t["ig_tile"]}">'
        + img_tag(images[al][n], P, alt_for(images[al][n], lang, titles[al]), "(max-width:860px) 33vw, 240px", cls="ph")
        + f'<span class="ig-ov"><img src="{ig_png}" width="34" height="34" alt=""></span></a>' for al, n in picks)
    ig_sec = f'''<section class="sec ig" id="instagram"><div class="wrap ig-grid">
<div class="ig-side rv"><div class="sec-head" style="margin-bottom:28px"><span class="eyebrow">{t["ig_eyebrow"]}</span><h2>{t["ig_h2"]}</h2><p>{t["ig_p"]}</p></div>
<div class="ig-card"><div class="ig-prof"><span class="ig-av"><span><img src="{P}img/brand/logo-bambu.svg" width="60" height="22" alt=""></span></span><div><b>@bambu.ubatuba</b><small>{t["ig_name"]}</small><small>Praia Grande · Ubatuba – SP</small></div></div>
<a class="btn btn-ig" href="{INSTAGRAM}" target="_blank" rel="noopener"><img src="{ig_png}" width="18" height="18" alt="">{t["ig_follow"]}</a></div></div>
<div class="ig-feed rv">{tiles}</div>
</div></section>'''

    # --- Como reservar ---
    steps = "".join(f'<li class="rv"><h3>{a}</h3><p>{b}</p></li>' for a, b in t["steps"])
    book_sec = f'''<section class="sec" id="reservar" style="padding-top:0;background:var(--mist)"><div class="wrap">
<div class="sec-head center rv"><span class="eyebrow">{t["bk_eyebrow"]}</span><h2>{t["bk_h2"]}</h2></div>
<ol class="steps">{steps}</ol>
<div class="book-cta"><a class="btn btn-wa" href="{wa_link(t["wa_msg"])}" target="_blank" rel="noopener">{WA}{t["wa_btn"]}</a></div>
</div></section>'''

    # --- Localização ---
    near = "".join(f"<li>{n}</li>" for n in t["near"])
    loc_sec = f'''<section class="sec loc" id="localizacao"><div class="wrap loc-grid">
<div class="rv"><div class="sec-head" style="margin-bottom:0"><span class="eyebrow">{t["loc_eyebrow"]}</span><h2>{t["loc_h2"]}</h2><p>{t["loc_p"]}</p></div>
<div class="places">
<a class="place" href="{MAPS["bambu"]}" target="_blank" rel="noopener"><span class="pin">{PIN}</span><span><b>{t["condos"]["bambu"][0]}</b><span>{t["loc_bambu"]}</span></span><span class="go">{t["open_maps"]} →</span></a>
<a class="place" href="{MAPS["dna"]}" target="_blank" rel="noopener"><span class="pin">{PIN}</span><span><b>{t["condos"]["dna"][0]}</b><span>{t["loc_dna"]}</span></span><span class="go">{t["open_maps"]} →</span></a>
</div>
<ul class="near">{near}</ul></div>
<div class="map rv"><iframe src="{MAP_EMBED}" title="{t["map_title"]}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div>
</div></section>'''

    # --- FAQ ---
    faq = "".join(f"<details><summary>{q}</summary><p>{r}</p></details>" for q, r in t["faq"])
    faq_sec = f'''<section class="sec" id="duvidas"><div class="wrap">
<div class="sec-head center rv"><span class="eyebrow">{t["faq_eyebrow"]}</span><h2>{t["faq_h2"]}</h2></div>
<div class="faq-list rv">{faq}</div></div></section>'''

    # --- CTA final ---
    bg = images["lazer-bambu"][2]
    final_sec = f'''<section class="sec final" id="contato">
<img src="{P}{bg["src"]}" width="{bg["w"]}" height="{bg["h"]}" alt="" loading="lazy" decoding="async">
<div class="wrap rv"><span class="eyebrow">{t["fn_eyebrow"]}</span><h2>{t["fn_h2"]}</h2><p>{t["fn_p"]}</p>
<div class="hero-cta"><a class="btn btn-wa" href="{wa_link(t["wa_msg"])}" target="_blank" rel="noopener">{WA}{t["wa_btn"]}</a><a class="btn btn-light" href="{INSTAGRAM}" target="_blank" rel="noopener">{IG}{t["follow"]}</a></div>
</div></section>'''

    # --- Rodapé ---
    yr = date.today().year
    ft_apts = "".join(f'<li><a href="#{a["key"]}">{titles[a["key"]]}</a></li>' for a in APTS)
    ft_nav = "".join(f'<li><a href="#{i}">{n}</a></li>' for i, n in zip(ids, t["nav"]))
    footer = f'''<footer class="ftr"><div class="wrap">
<div class="ftr-grid">
<div><a class="logo" href="#top" aria-label="Bambu Ubatuba"><img src="{P}img/brand/logo-bambu-branco.svg" width="126" height="45" alt="Bambu Ubatuba" loading="lazy"></a><p>{t["ft_about"]}</p></div>
<div><h4>{t["ft_apts"]}</h4><ul>{ft_apts}</ul></div>
<div><h4>{t["ft_links"]}</h4><ul>{ft_nav}</ul></div>
<div><h4>{t["ft_contact"]}</h4><ul>
<li><a href="{wa_link(t["wa_msg"])}" target="_blank" rel="noopener">WhatsApp: +55 35 98827-5400</a></li>
<li><a href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram: @bambu.ubatuba</a></li>
{"".join(f'<li><a href="{a["airbnb"]}" target="_blank" rel="noopener">Airbnb · {a["name"]}</a></li>' for a in APTS)}
<li>Praia Grande · Ubatuba – SP</li></ul></div>
</div>
<div class="ftr-bot"><span>© {yr} Bambu Ubatuba. {t["rights"]}</span><span>Praia Grande · Ubatuba · São Paulo · Brasil</span></div>
</div></footer>
<a class="fab" href="{wa_link(t["wa_msg"])}" target="_blank" rel="noopener" aria-label="{t["wa_btn"]}">{WA}</a>
<div class="lb" role="dialog" aria-modal="true" aria-hidden="true" aria-label="Galeria">
<div class="lb-top"><div><b></b> <span class="lb-count"></span></div><button class="lb-close" aria-label="{t["lb_close"]}">{CLOSE}</button></div>
<div class="lb-stage"><img alt=""><button class="lb-prev" aria-label="{t["lb_prev"]}">{PREV}</button><button class="lb-next" aria-label="{t["lb_next"]}">{NEXT}</button></div>
<p class="lb-cap"></p></div>
<script type="application/json" id="albums">{json.dumps(albums, ensure_ascii=False, separators=(",", ":"))}</script>
<script src="{P}js/main.js" defer></script>'''

    body = (f'<body>{header}<main id="main">{hero_html}{trust}{apts_sec}{lazer_sec}{rev_sec}{ig_sec}{book_sec}{loc_sec}{faq_sec}{final_sec}</main>{footer}</body></html>')
    return head + "\n" + body


def main():
    with open(os.path.join(ROOT, "tools", "images.json")) as f:
        images = json.load(f)
    with open(os.path.join(ROOT, "tools", "src", "style.css")) as f:
        css = minify_css(f.read())
    for lang in LANGS:
        out = os.path.join(SITE, PATH[lang].strip("/"), "index.html")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        html = build(lang, images, css)
        with open(out, "w", encoding="utf-8") as f:
            f.write(html)
        print(out, f"{len(html.encode()) / 1024:.1f} KB")

    today = date.today().isoformat()
    urls = []
    for l in LANGS:
        alts = "".join(f'<xhtml:link rel="alternate" hreflang="{HREFLANG[x]}" href="{SITE_URL}{PATH[x]}"/>' for x in LANGS)
        alts += f'<xhtml:link rel="alternate" hreflang="x-default" href="{SITE_URL}/"/>'
        imgs = "".join(f"<image:image><image:loc>{SITE_URL}/{it['src']}</image:loc></image:image>"
                       for k in images for it in images[k][:6]) if l == "pt" else ""
        urls.append(f"<url><loc>{SITE_URL}{PATH[l]}</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq>"
                    f"<priority>{'1.0' if l == 'pt' else '0.8'}</priority>{alts}{imgs}</url>")
    with open(os.path.join(SITE, "sitemap.xml"), "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
                'xmlns:xhtml="http://www.w3.org/1999/xhtml" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">'
                + "".join(urls) + "</urlset>\n")
    with open(os.path.join(SITE, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n")
    with open(os.path.join(SITE, "favicon.svg"), "w") as f:
        f.write(LOGO.replace('aria-hidden="true"', 'xmlns="http://www.w3.org/2000/svg"'))
    with open(os.path.join(SITE, "site.webmanifest"), "w") as f:
        json.dump({"name": "Bambu Ubatuba", "short_name": "Bambu", "start_url": "/", "display": "standalone",
                   "background_color": "#f8f6f1", "theme_color": "#062c42",
                   "icons": [{"src": "/apple-touch-icon.png", "sizes": "180x180", "type": "image/png"}]}, f)


def minify_css(css):
    import re
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{}:;,>])\s*", r"\1", css)
    return css.replace(";}", "}").strip()


if __name__ == "__main__":
    main()

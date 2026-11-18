# Site Bambu Ubatuba

Site estático em 3 idiomas, gerado a partir de `tools/`.

- `site/`: **pasta para publicar** (envie todo o conteúdo para a raiz do domínio).
  - `index.html` (Português), `en/index.html` (English), `es/index.html` (Español)
  - `img/` (fotos em WebP), `fonts/`, `js/main.js`, `sitemap.xml`, `robots.txt`, ícones
- `tools/build.py`: textos, traduções, links e configurações. Gera os HTML.
- `tools/optimize_images.py`: escolhe, ordena e converte as fotos das pastas originais.
- `tools/src/style.css`: estilos (inseridos direto no HTML no build).

## Alterar algo

1. Edite `tools/build.py` (topo do arquivo: domínio, WhatsApp, links do Maps e avaliações em destaque).
2. Rode `python3 tools/build.py`.
3. Para trocar fotos ou a ordem delas: edite as listas em `tools/optimize_images.py` e rode
   `python3 tools/optimize_images.py` (precisa de `pip install pillow`), depois rode o build.

## Antes de publicar

- [ ] Trocar `SITE_URL` pelo domínio definitivo (é usado no canonical, hreflang, sitemap e Open Graph).
- [ ] Trocar os links `MAPS` pelos links "Compartilhar" do Google Maps com o pino exato de cada prédio.
- [ ] Colar as melhores avaliações reais do Airbnb em `REVIEWS`.
- [ ] Publicar com HTTPS e compressão gzip/brotli (Netlify, Vercel, Cloudflare Pages ou Hostinger fazem isso automaticamente).
- [ ] Cadastrar o site no Google Search Console e enviar `sitemap.xml`.
- [ ] Criar o Perfil da Empresa no Google (Google Meu Negócio) com o link do site. Isso pesa muito nas buscas locais ("aluguel temporada Ubatuba").
- [ ] Colocar o link do site na bio do Instagram.

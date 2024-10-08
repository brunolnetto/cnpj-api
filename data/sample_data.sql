--
-- PostgreSQL database dump
--

-- Dumped from database version 13.15
-- Dumped by pg_dump version 13.15

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: cnae; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cnae (
    codigo text,
    descricao text
);


ALTER TABLE public.cnae OWNER TO postgres;

--
-- Name: empresa; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.empresa (
    cnpj_basico text,
    razao_social text,
    natureza_juridica text,
    qualificacao_responsavel text,
    capital_social text,
    porte_empresa text,
    ente_federativo_responsavel text
);


ALTER TABLE public.empresa OWNER TO postgres;

--
-- Name: estabelecimento; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.estabelecimento (
    cnpj_basico text,
    cnpj_ordem text,
    cnpj_dv text,
    identificador_matriz_filial text,
    nome_fantasia text,
    situacao_cadastral text,
    data_situacao_cadastral text,
    motivo_situacao_cadastral text,
    nome_cidade_exterior text,
    pais text,
    data_inicio_atividade text,
    cnae_fiscal_principal text,
    cnae_fiscal_secundaria text,
    tipo_logradouro text,
    logradouro text,
    numero text,
    complemento text,
    bairro text,
    cep text,
    uf text,
    municipio text,
    ddd_1 text,
    telefone_1 text,
    ddd_2 text,
    telefone_2 text,
    ddd_fax text,
    fax text,
    correio_eletronico text,
    situacao_especial text,
    data_situacao_especial text
);


ALTER TABLE public.estabelecimento OWNER TO postgres;

--
-- Name: moti; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.moti (
    codigo text,
    descricao text
);


ALTER TABLE public.moti OWNER TO postgres;

--
-- Name: munic; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.munic (
    codigo text,
    descricao text
);


ALTER TABLE public.munic OWNER TO postgres;

--
-- Name: natju; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.natju (
    codigo text NOT NULL,
    descricao text
);


ALTER TABLE public.natju OWNER TO postgres;

--
-- Name: pais; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pais (
    codigo text,
    descricao text
);


ALTER TABLE public.pais OWNER TO postgres;

--
-- Name: quals; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.quals (
    codigo text,
    descricao text
);


ALTER TABLE public.quals OWNER TO postgres;

--
-- Name: simples; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.simples (
    cnpj_basico text,
    opcao_pelo_simples text,
    data_opcao_simples text,
    data_exclusao_simples text,
    opcao_mei text,
    data_opcao_mei text,
    data_exclusao_mei text
);


ALTER TABLE public.simples OWNER TO postgres;

--
-- Name: socios; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.socios (
    cnpj_basico text,
    identificador_socio text,
    nome_socio_razao_social text,
    cpf_cnpj_socio text,
    qualificacao_socio text,
    data_entrada_sociedade text,
    pais text,
    representante_legal text,
    nome_do_representante text,
    qualificacao_representante_legal text,
    faixa_etaria text
);


ALTER TABLE public.socios OWNER TO postgres;

--
-- Data for Name: audit; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.audit (audi_id, audi_created_at, audi_table_name, audi_filenames, audi_file_size_bytes, audi_source_updated_at, audi_downloaded_at, audi_processed_at, audi_inserted_at) FROM stdin;
\.


--
-- Data for Name: cnae; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cnae (codigo, descricao) FROM stdin;
111301	Cultivo de arroz
111302	Cultivo de milho
111303	Cultivo de trigo
111399	Cultivo de outros cereais não especificados anteriormente
112101	Cultivo de algodão herbáceo
112102	Cultivo de juta
112199	Cultivo de outras fibras de lavoura temporária não especificadas anteriormente
113000	Cultivo de cana-de-açúcar
114800	Cultivo de fumo
115600	Cultivo de soja
116401	Cultivo de amendoim
116402	Cultivo de girassol
116403	Cultivo de mamona
116499	Cultivo de outras oleaginosas de lavoura temporária não especificadas anteriormente
119901	Cultivo de abacaxi
119902	Cultivo de alho
119903	Cultivo de batata-inglesa
119904	Cultivo de cebola
119905	Cultivo de feijão
119906	Cultivo de mandioca
119907	Cultivo de melão
119908	Cultivo de melancia
119909	Cultivo de tomate rasteiro
119999	Cultivo de outras plantas de lavoura temporária não especificadas anteriormente
121101	Horticultura, exceto morango
121102	Cultivo de morango
122900	Cultivo de flores e plantas ornamentais
131800	Cultivo de laranja
132600	Cultivo de uva
133401	Cultivo de açaí
133402	Cultivo de banana
133403	Cultivo de caju
133404	Cultivo de cítricos, exceto laranja
133405	Cultivo de coco-da-baía
133406	Cultivo de guaraná
133407	Cultivo de maçã
133408	Cultivo de mamão
133409	Cultivo de maracujá
133410	Cultivo de manga
133411	Cultivo de pêssego
133499	Cultivo de frutas de lavoura permanente não especificadas anteriormente
134200	Cultivo de café
135100	Cultivo de cacau
139301	Cultivo de chá-da-índia
139302	Cultivo de erva-mate
139303	Cultivo de pimenta-do-reino
139304	Cultivo de plantas para condimento, exceto pimenta-do-reino
139305	Cultivo de dendê
139306	Cultivo de seringueira
139399	Cultivo de outras plantas de lavoura permanente não especificadas anteriormente
141501	Produção de sementes certificadas, exceto de forrageiras para pasto
141502	Produção de sementes certificadas de forrageiras para formação de pasto
142300	Produção de mudas e outras formas de propagação vegetal, certificadas
151201	Criação de bovinos para corte
151202	Criação de bovinos para leite
151203	Criação de bovinos, exceto para corte e leite
152101	Criação de bufalinos
152102	Criação de eqüinos
152103	Criação de asininos e muares
153901	Criação de caprinos
153902	Criação de ovinos, inclusive para produção de lã
154700	Criação de suínos
155501	Criação de frangos para corte
155502	Produção de pintos de um dia
155503	Criação de outros galináceos, exceto para corte
155504	Criação de aves, exceto galináceos
155505	Produção de ovos
159801	Apicultura
159802	Criação de animais de estimação
159803	Criação de escargô
159804	Criação de bicho-da-seda
159899	Criação de outros animais não especificados anteriormente
161001	Serviço de pulverização e controle de pragas agrícolas
161002	Serviço de poda de árvores para lavouras
161003	Serviço de preparação de terreno, cultivo e colheita
161099	Atividades de apoio à agricultura não especificadas anteriormente
162801	Serviço de inseminação artificial em animais
162802	Serviço de tosquiamento de ovinos
162803	Serviço de manejo de animais
162899	Atividades de apoio à pecuária não especificadas anteriormente
163600	Atividades de pós-colheita
170900	Caça e serviços relacionados
210101	Cultivo de eucalipto
210102	Cultivo de acácia-negra
210103	Cultivo de pinus
210104	Cultivo de teca
210105	Cultivo de espécies madeireiras, exceto eucalipto, acácia-negra, pinus e teca
210106	Cultivo de mudas em viveiros florestais
210107	Extração de madeira em florestas plantadas
210108	Produção de carvão vegetal - florestas plantadas
210109	Produção de casca de acácia-negra - florestas plantadas
210199	Produção de produtos não-madeireiros não especificados anteriormente em florestas plantadas
220901	Extração de madeira em florestas nativas
220902	Produção de carvão vegetal - florestas nativas
220903	Coleta de castanha-do-pará em florestas nativas
220904	Coleta de látex em florestas nativas
220905	Coleta de palmito em florestas nativas
220906	Conservação de florestas nativas
220999	Coleta de produtos não-madeireiros não especificados anteriormente em florestas nativas
230600	Atividades de apoio à produção florestal
311601	Pesca de peixes em água salgada
311602	Pesca de crustáceos e moluscos em água salgada
311603	Coleta de outros produtos marinhos
311604	Atividades de apoio à pesca em água salgada
312401	Pesca de peixes em água doce
312402	Pesca de crustáceos e moluscos em água doce
312403	Coleta de outros produtos aquáticos de água doce
312404	Atividades de apoio à pesca em água doce
321301	Criação de peixes em água salgada e salobra
321302	Criação de camarões em água salgada e salobra
321303	Criação de ostras e mexilhões em água salgada e salobra
321304	Criação de peixes ornamentais em água salgada e salobra
321305	Atividades de apoio à aqüicultura em água salgada e salobra
321399	Cultivos e semicultivos da aqüicultura em água salgada e salobra não especificados anteriormente
322101	Criação de peixes em água doce
322102	Criação de camarões em água doce
322103	Criação de ostras e mexilhões em água doce
322104	Criação de peixes ornamentais em água doce
322105	Ranicultura
322106	Criação de jacaré
322107	Atividades de apoio à aqüicultura em água doce
322199	Cultivos e semicultivos da aqüicultura em água doce não especificados anteriormente
500301	Extração de carvão mineral
500302	Beneficiamento de carvão mineral
600001	Extração de petróleo e gás natural
600002	Extração e beneficiamento de xisto
600003	Extração e beneficiamento de areias betuminosas
710301	Extração de minério de ferro
710302	Pelotização, sinterização e outros beneficiamentos de minério de ferro
721901	Extração de minério de alumínio
721902	Beneficiamento de minério de alumínio
722701	Extração de minério de estanho
722702	Beneficiamento de minério de estanho
723501	Extração de minério de manganês
723502	Beneficiamento de minério de manganês
724301	Extração de minério de metais preciosos
724302	Beneficiamento de minério de metais preciosos
725100	Extração de minerais radioativos
729401	Extração de minérios de nióbio e titânio
729402	Extração de minério de tungstênio
729403	Extração de minério de níquel
729404	Extração de minérios de cobre, chumbo, zinco e outros minerais metálicos não-ferrosos não especificados anteriormente
729405	Beneficiamento de minérios de cobre, chumbo, zinco e outros minerais metálicos não-ferrosos não especificados anteriormente
810001	Extração de ardósia e beneficiamento associado
810002	Extração de granito e beneficiamento associado
810003	Extração de mármore e beneficiamento associado
810004	Extração de calcário e dolomita e beneficiamento associado
810005	Extração de gesso e caulim
810006	Extração de areia, cascalho ou pedregulho e beneficiamento associado
810007	Extração de argila e beneficiamento associado
810008	Extração de saibro e beneficiamento associado
810009	Extração de basalto e beneficiamento associado
810010	Beneficiamento de gesso e caulim associado à extração
810099	Extração e britamento de pedras e outros materiais para construção e beneficiamento associado
891600	Extração de minerais para fabricação de adubos, fertilizantes e outros produtos químicos
892401	Extração de sal marinho
892402	Extração de sal-gema
892403	Refino e outros tratamentos do sal
893200	Extração de gemas (pedras preciosas e semipreciosas)
899101	Extração de grafita
899102	Extração de quartzo
899103	Extração de amianto
899199	Extração de outros minerais não-metálicos não especificados anteriormente
910600	Atividades de apoio à extração de petróleo e gás natural
990401	Atividades de apoio à extração de minério de ferro
990402	Atividades de apoio à extração de minerais metálicos não-ferrosos
990403	Atividades de apoio à extração de minerais não-metálicos
1011201	Frigorífico - abate de bovinos
1011202	Frigorífico - abate de eqüinos
1011203	Frigorífico - abate de ovinos e caprinos
1011204	Frigorífico - abate de bufalinos
1011205	Matadouro - abate de reses sob contrato - exceto abate de suínos
1012101	Abate de aves
1012102	Abate de pequenos animais
1012103	Frigorífico - abate de suínos
1012104	Matadouro - abate de suínos sob contrato
1013901	Fabricação de produtos de carne
1013902	Preparação de subprodutos do abate
1020101	Preservação de peixes, crustáceos e moluscos
1020102	Fabricação de conservas de peixes, crustáceos e moluscos
1031700	Fabricação de conservas de frutas
1032501	Fabricação de conservas de palmito
1032599	Fabricação de conservas de legumes e outros vegetais, exceto palmito
1033301	Fabricação de sucos concentrados de frutas, hortaliças e legumes
1033302	Fabricação de sucos de frutas, hortaliças e legumes, exceto concentrados
1041400	Fabricação de óleos vegetais em bruto, exceto óleo de milho
1042200	Fabricação de óleos vegetais refinados, exceto óleo de milho
1043100	Fabricação de margarina e outras gorduras vegetais e de óleos não-comestíveis de animais
1051100	Preparação do leite
1052000	Fabricação de laticínios
1053800	Fabricação de sorvetes e outros gelados comestíveis
1061901	Beneficiamento de arroz
1061902	Fabricação de produtos do arroz
1062700	Moagem de trigo e fabricação de derivados
1063500	Fabricação de farinha de mandioca e derivados
1064300	Fabricação de farinha de milho e derivados, exceto óleos de milho
1065101	Fabricação de amidos e féculas de vegetais
1065102	Fabricação de óleo de milho em bruto
1065103	Fabricação de óleo de milho refinado
1066000	Fabricação de alimentos para animais
1069400	Moagem e fabricação de produtos de origem vegetal não especificados anteriormente
1071600	Fabricação de açúcar em bruto
1072401	Fabricação de açúcar de cana refinado
1072402	Fabricação de açúcar de cereais (dextrose) e de beterraba
1081301	Beneficiamento de café
1081302	Torrefação e moagem de café
1082100	Fabricação de produtos à base de café
1091100	Fabricação de produtos de panificação
1091101	Fabricação de produtos de panificação industrial
1091102	Fabricação de produtos de padaria e confeitaria com predominância de produção própria
1092900	Fabricação de biscoitos e bolachas
1093701	Fabricação de produtos derivados do cacau e de chocolates
1093702	Fabricação de frutas cristalizadas, balas e semelhantes
1094500	Fabricação de massas alimentícias
1095300	Fabricação de especiarias, molhos, temperos e condimentos
1096100	Fabricação de alimentos e pratos prontos
1099601	Fabricação de vinagres
1099602	Fabricação de pós alimentícios
1099603	Fabricação de fermentos e leveduras
1099604	Fabricação de gelo comum
1099605	Fabricação de produtos para infusão (chá, mate, etc.)
1099606	Fabricação de adoçantes naturais e artificiais
1099607	Fabricação de alimentos dietéticos e complementos alimentares
1099699	Fabricação de outros produtos alimentícios não especificados anteriormente
1111901	Fabricação de aguardente de cana-de-açúcar
1111902	Fabricação de outras aguardentes e bebidas destiladas
1112700	Fabricação de vinho
1113501	Fabricação de malte, inclusive malte uísque
1113502	Fabricação de cervejas e chopes
1121600	Fabricação de águas envasadas
1122401	Fabricação de refrigerantes
1122402	Fabricação de chá mate e outros chás prontos para consumo
1122403	Fabricação de refrescos, xaropes e pós para refrescos, exceto refrescos de frutas
1122404	Fabricação de bebidas isotônicas
1122499	Fabricação de outras bebidas não-alcoólicas não especificadas anteriormente
1210700	Processamento industrial do fumo
1220401	Fabricação de cigarros
1220402	Fabricação de cigarrilhas e charutos
1220403	Fabricação de filtros para cigarros
1220499	Fabricação de outros produtos do fumo, exceto cigarros, cigarrilhas e charutos
1311100	Preparação e fiação de fibras de algodão
1312000	Preparação e fiação de fibras têxteis naturais, exceto algodão
1313800	Fiação de fibras artificiais e sintéticas
1314600	Fabricação de linhas para costurar e bordar
1321900	Tecelagem de fios de algodão
1322700	Tecelagem de fios de fibras têxteis naturais, exceto algodão
1323500	Tecelagem de fios de fibras artificiais e sintéticas
1330800	Fabricação de tecidos de malha
1340501	Estamparia e texturização em fios, tecidos, artefatos têxteis e peças do vestuário
1340502	Alvejamento, tingimento e torção em fios, tecidos, artefatos têxteis e peças do vestuário
1340599	Outros serviços de acabamento em fios, tecidos, artefatos têxteis e peças do vestuário
1351100	Fabricação de artefatos têxteis para uso doméstico
1352900	Fabricação de artefatos de tapeçaria
1353700	Fabricação de artefatos de cordoaria
1354500	Fabricação de tecidos especiais, inclusive artefatos
1359600	Fabricação de outros produtos têxteis não especificados anteriormente
1411801	Confecção de roupas íntimas
1411802	Facção de roupas íntimas
1412601	Confecção de peças de vestuário, exceto roupas íntimas e as confeccionadas sob medida
1412602	Confecção, sob medida, de peças do vestuário, exceto roupas íntimas
1412603	Facção de peças do vestuário, exceto roupas íntimas
1413401	Confecção de roupas profissionais, exceto sob medida
1413402	Confecção, sob medida, de roupas profissionais
1413403	Facção de roupas profissionais
1414200	Fabricação de acessórios do vestuário, exceto para segurança e proteção
1421500	Fabricação de meias
1422300	Fabricação de artigos do vestuário, produzidos em malharias e tricotagens, exceto meias
1510600	Curtimento e outras preparações de couro
1521100	Fabricação de artigos para viagem, bolsas e semelhantes de qualquer material
1529700	Fabricação de artefatos de couro não especificados anteriormente
1531901	Fabricação de calçados de couro
1531902	Acabamento de calçados de couro sob contrato
1532700	Fabricação de tênis de qualquer material
1533500	Fabricação de calçados de material sintético
1539400	Fabricação de calçados de materiais não especificados anteriormente
1540800	Fabricação de partes para calçados, de qualquer material
1610201	Serrarias com desdobramento de madeira
1610202	Serrarias sem desdobramento de madeira
1610203	Serrarias com desdobramento de madeira em bruto
1610204	Serrarias sem desdobramento de madeira em bruto  -Resserragem
1610205	Serviço de tratamento de madeira realizado sob contrato
1621800	Fabricação de madeira laminada e de chapas de madeira compensada, prensada e aglomerada
1622601	Fabricação de casas de madeira pré-fabricadas
1622602	Fabricação de esquadrias de madeira e de peças de madeira para instalações industriais e comerciais
1622699	Fabricação de outros artigos de carpintaria para construção
1623400	Fabricação de artefatos de tanoaria e de embalagens de madeira
1629301	Fabricação de artefatos diversos de madeira, exceto móveis
1629302	Fabricação de artefatos diversos de cortiça, bambu, palha, vime e outros materiais trançados, exceto móveis
1710900	Fabricação de celulose e outras pastas para a fabricação de papel
1721400	Fabricação de papel
1722200	Fabricação de cartolina e papel-cartão
1731100	Fabricação de embalagens de papel
1732000	Fabricação de embalagens de cartolina e papel-cartão
1733800	Fabricação de chapas e de embalagens de papelão ondulado
1741901	Fabricação de formulários contínuos
1741902	Fabricação de produtos de papel, cartolina, papel cartão e papelão ondulado para uso comercial e de escritório, exceto formulário contínuo
1742701	Fabricação de fraldas descartáveis
1742702	Fabricação de absorventes higiênicos
1742799	Fabricação de produtos de papel para uso doméstico e higiênico-sanitário não especificados anteriormente
1749400	Fabricação de produtos de pastas celulósicas, papel, cartolina, papel-cartão e papelão ondulado não especificados anteriormente
1811301	Impressão de jornais
1811302	Impressão de livros, revistas e outras publicações periódicas
1812100	Impressão de material de segurança
1813001	Impressão de material para uso publicitário
1813099	Impressão de material para outros usos
1821100	Serviços de pré-impressão
1822900	Serviços de acabamentos gráficos
1822901	Serviços de encadernação e plastificação
1822999	Serviços de acabamentos gráficos, exceto encadernação e plastificação
1830001	Reprodução de som em qualquer suporte
1830002	Reprodução de vídeo em qualquer suporte
1830003	Reprodução de software em qualquer suporte
1910100	Coquerias
1921700	Fabricação de produtos do refino de petróleo
1922501	Formulação de combustíveis
1922502	Rerrefino de óleos lubrificantes
1922599	Fabricação de outros produtos derivados do petróleo, exceto produtos do refino
1931400	Fabricação de álcool
1932200	Fabricação de biocombustíveis, exceto álcool
2011800	Fabricação de cloro e álcalis
2012600	Fabricação de intermediários para fertilizantes
2013400	Fabricação de adubos e fertilizantes
2013401	Fabricação de adubos e fertilizantes organo-minerais
2013402	Fabricação de adubos e fertilizantes, exceto organo-minerais
2014200	Fabricação de gases industriais
2019301	Elaboração de combustíveis nucleares
2019399	Fabricação de outros produtos químicos inorgânicos não especificados anteriormente
2021500	Fabricação de produtos petroquímicos básicos
2022300	Fabricação de intermediários para plastificantes, resinas e fibras
2029100	Fabricação de produtos químicos orgânicos não especificados anteriormente
2031200	Fabricação de resinas termoplásticas
2032100	Fabricação de resinas termofixas
2033900	Fabricação de elastômeros
2040100	Fabricação de fibras artificiais e sintéticas
2051700	Fabricação de defensivos agrícolas
2052500	Fabricação de desinfestantes domissanitários
2061400	Fabricação de sabões e detergentes sintéticos
2062200	Fabricação de produtos de limpeza e polimento
2063100	Fabricação de cosméticos, produtos de perfumaria e de higiene pessoal
2071100	Fabricação de tintas, vernizes, esmaltes e lacas
2072000	Fabricação de tintas de impressão
2073800	Fabricação de impermeabilizantes, solventes e produtos afins
2091600	Fabricação de adesivos e selantes
2092401	Fabricação de pólvoras, explosivos e detonantes
2092402	Fabricação de artigos pirotécnicos
2092403	Fabricação de fósforos de segurança
2093200	Fabricação de aditivos de uso industrial
2094100	Fabricação de catalisadores
2099101	Fabricação de chapas, filmes, papéis e outros materiais e produtos químicos para fotografia
2099199	Fabricação de outros produtos químicos não especificados anteriormente
2110600	Fabricação de produtos farmoquímicos
2121101	Fabricação de medicamentos alopáticos para uso humano
2121102	Fabricação de medicamentos homeopáticos para uso humano
2121103	Fabricação de medicamentos fitoterápicos para uso humano
2122000	Fabricação de medicamentos para uso veterinário
2123800	Fabricação de preparações farmacêuticas
2211100	Fabricação de pneumáticos e de câmaras-de-ar
2212900	Reforma de pneumáticos usados
2219600	Fabricação de artefatos de borracha não especificados anteriormente
2221800	Fabricação de laminados planos e tubulares de material plástico
2222600	Fabricação de embalagens de material plástico
2223400	Fabricação de tubos e acessórios de material plástico para uso na construção
2229301	Fabricação de artefatos de material plástico para uso pessoal e doméstico
2229302	Fabricação de artefatos de material plástico para usos industriais
2229303	Fabricação de artefatos de material plástico para uso na construção, exceto tubos e acessórios
2229399	Fabricação de artefatos de material plástico para outros usos não especificados anteriormente
2311700	Fabricação de vidro plano e de segurança
2312500	Fabricação de embalagens de vidro
2319200	Fabricação de artigos de vidro
2320600	Fabricação de cimento
2330301	Fabricação de estruturas pré-moldadas de concreto armado, em série e sob encomenda
2330302	Fabricação de artefatos de cimento para uso na construção
2330303	Fabricação de artefatos de fibrocimento para uso na construção
2330304	Fabricação de casas pré-moldadas de concreto
2330305	Preparação de massa de concreto e argamassa para construção
2330399	Fabricação de outros artefatos e produtos de concreto, cimento, fibrocimento, gesso e materiais semelhantes
5911101	Estúdios cinematográficos
2341900	Fabricação de produtos cerâmicos refratários
2342701	Fabricação de azulejos e pisos
2342702	Fabricação de artefatos de cerâmica e barro cozido para uso na construção, exceto azulejos e pisos
2349401	Fabricação de material sanitário de cerâmica
2349499	Fabricação de produtos cerâmicos não-refratários não especificados anteriormente
2391501	Britamento de pedras, exceto associado à extração
2391502	Aparelhamento de pedras para construção, exceto associado à extração
2391503	Aparelhamento de placas e execução de trabalhos em mármore, granito, ardósia e outras pedras
2392300	Fabricação de cal e gesso
2399101	Decoração, lapidação, gravação, vitrificação e outros trabalhos em cerâmica, louça, vidro e cristal
2399102	Fabricação de abrasivos
2399199	Fabricação de outros produtos de minerais não-metálicos não especificados anteriormente
2411300	Produção de ferro-gusa
2412100	Produção de ferroligas
2421100	Produção de semi-acabados de aço
2422901	Produção de laminados planos de aço ao carbono, revestidos ou não
2422902	Produção de laminados planos de aços especiais
2423701	Produção de tubos de aço sem costura
2423702	Produção de laminados longos de aço, exceto tubos
2424501	Produção de arames de aço
2424502	Produção de relaminados, trefilados e perfilados de aço, exceto arames
2431800	Produção de tubos de aço com costura
2439300	Produção de outros tubos de ferro e aço
2441501	Produção de alumínio e suas ligas em formas primárias
2441502	Produção de laminados de alumínio
2442300	Metalurgia dos metais preciosos
2443100	Metalurgia do cobre
2449101	Produção de zinco em formas primárias
2449102	Produção de laminados de zinco
2449103	Fabricação de ânodos para galvanoplastia
2449199	Metalurgia de outros metais não-ferrosos e suas ligas não especificados anteriormente
2451200	Fundição de ferro e aço
2452100	Fundição de metais não-ferrosos e suas ligas
2511000	Fabricação de estruturas metálicas
2512800	Fabricação de esquadrias de metal
2513600	Fabricação de obras de caldeiraria pesada
2521700	Fabricação de tanques, reservatórios metálicos e caldeiras para aquecimento central
2522500	Fabricação de caldeiras geradoras de vapor, exceto para aquecimento central e para veículos
2531401	Produção de forjados de aço
2531402	Produção de forjados de metais não-ferrosos e suas ligas
2532201	Produção de artefatos estampados de metal
2532202	Metalurgia do pó
2539000	Serviços de usinagem, solda, tratamento e revestimento em metais
2539001	Serviços de usinagem, tornearia e solda
2539002	Serviços de tratamento e revestimento em metais
2541100	Fabricação de artigos de cutelaria
2542000	Fabricação de artigos de serralheria, exceto esquadrias
2543800	Fabricação de ferramentas
2550101	Fabricação de equipamento bélico pesado, exceto veículos militares de combate
2550102	Fabricação de armas de fogo, outras armas e munições
2591800	Fabricação de embalagens metálicas
2592601	Fabricação de produtos de trefilados de metal padronizados
2592602	Fabricação de produtos de trefilados de metal, exceto padronizados
2593400	Fabricação de artigos de metal para uso doméstico e pessoal
2599301	Serviços de confecção de armações metálicas para a construção
2599302	Serviço de corte e dobra de metais
2599399	Fabricação de outros produtos de metal não especificados anteriormente
2610800	Fabricação de componentes eletrônicos
2621300	Fabricação de equipamentos de informática
2622100	Fabricação de periféricos para equipamentos de informática
2631100	Fabricação de equipamentos transmissores de comunicação, peças e acessórios
2632900	Fabricação de aparelhos telefônicos e de outros equipamentos de comunicação, peças e acessórios
2640000	Fabricação de aparelhos de recepção, reprodução, gravação e amplificação de áudio e vídeo
2651500	Fabricação de aparelhos e equipamentos de medida, teste e controle
2652300	Fabricação de cronômetros e relógios
2660400	Fabricação de aparelhos eletromédicos e eletroterapêuticos e equipamentos de irradiação
2670101	Fabricação de equipamentos e instrumentos ópticos, peças e acessórios
2670102	Fabricação de aparelhos fotográficos e cinematográficos, peças e acessórios
2680900	Fabricação de mídias virgens, magnéticas e ópticas
2710401	Fabricação de geradores de corrente contínua e alternada, peças e acessórios
2710402	Fabricação de transformadores, indutores, conversores, sincronizadores e semelhantes, peças e acessórios
2710403	Fabricação de motores elétricos, peças e acessórios
2721000	Fabricação de pilhas, baterias e acumuladores elétricos, exceto para veículos automotores
2722801	Fabricação de baterias e acumuladores para veículos automotores
2722802	Recondicionamento de baterias e acumuladores para veículos automotores
2731700	Fabricação de aparelhos e equipamentos para distribuição e controle de energia elétrica
2732500	Fabricação de material elétrico para instalações em circuito de consumo
2733300	Fabricação de fios, cabos e condutores elétricos isolados
2740601	Fabricação de lâmpadas
2740602	Fabricação de luminárias e outros equipamentos de iluminação
2751100	Fabricação de fogões, refrigeradores e máquinas de lavar e secar para uso doméstico, peças e acessórios
2759701	Fabricação de aparelhos elétricos de uso pessoal, peças e acessórios
2759799	Fabricação de outros aparelhos eletrodomésticos não especificados anteriormente, peças e acessórios
2790201	Fabricação de eletrodos, contatos e outros artigos de carvão e grafita para uso elétrico, eletroímãs e isoladores
2790202	Fabricação de equipamentos para sinalização e alarme
2790299	Fabricação de outros equipamentos e aparelhos elétricos não especificados anteriormente
2811900	Fabricação de motores e turbinas, peças e acessórios, exceto para aviões e veículos rodoviários
2812700	Fabricação de equipamentos hidráulicos e pneumáticos, peças e acessórios, exceto válvulas
2813500	Fabricação de válvulas, registros e dispositivos semelhantes, peças e acessórios
2814301	Fabricação de compressores para uso industrial, peças e acessórios
2814302	Fabricação de compressores para uso não industrial, peças e acessórios
2815101	Fabricação de rolamentos para fins industriais
2815102	Fabricação de equipamentos de transmissão para fins industriais, exceto rolamentos
2821601	Fabricação de fornos industriais, aparelhos e equipamentos não-elétricos para instalações térmicas, peças e acessórios
2821602	Fabricação de estufas e fornos elétricos para fins industriais, peças e acessórios
2822401	Fabricação de máquinas, equipamentos e aparelhos para transporte e elevação de pessoas, peças e acessórios
2822402	Fabricação de máquinas, equipamentos e aparelhos para transporte e elevação de cargas, peças e acessórios
2823200	Fabricação de máquinas e aparelhos de refrigeração e ventilação para uso industrial e comercial, peças e acessórios
2824101	Fabricação de aparelhos e equipamentos de ar condicionado para uso industrial
2824102	Fabricação de aparelhos e equipamentos de ar condicionado para uso não-industrial
2825900	Fabricação de máquinas e equipamentos para saneamento básico e ambiental, peças e acessórios
2829101	Fabricação de máquinas de escrever, calcular e outros equipamentos não-eletrônicos para escritório, peças e acessórios
2829199	Fabricação de outras máquinas e equipamentos de uso geral não especificados anteriormente, peças e acessórios
2831300	Fabricação de tratores agrícolas, peças e acessórios
2832100	Fabricação de equipamentos para irrigação agrícola, peças e acessórios
2833000	Fabricação de máquinas e equipamentos para a agricultura e pecuária, peças e acessórios, exceto para irrigação
2840200	Fabricação de máquinas-ferramenta, peças e acessórios
2851800	Fabricação de máquinas e equipamentos para a prospecção e extração de petróleo, peças e acessórios
2852600	Fabricação de outras máquinas e equipamentos para uso na extração mineral, peças e acessórios, exceto na extração de petróleo
2853400	Fabricação de tratores, peças e acessórios, exceto agrícolas
2854200	Fabricação de máquinas e equipamentos para terraplenagem, pavimentação e construção, peças e acessórios, exceto tratores
2861500	Fabricação de máquinas para a indústria metalúrgica, peças e acessórios, exceto máquinas-ferramenta
2862300	Fabricação de máquinas e equipamentos para as indústrias de alimentos, bebidas e fumo, peças e acessórios
2863100	Fabricação de máquinas e equipamentos para a indústria têxtil, peças e acessórios
2864000	Fabricação de máquinas e equipamentos para as indústrias do vestuário, do couro e de calçados, peças e acessórios
2865800	Fabricação de máquinas e equipamentos para as indústrias de celulose, papel e papelão e artefatos, peças e acessórios
2866600	Fabricação de máquinas e equipamentos para a indústria do plástico, peças e acessórios
2869100	Fabricação de máquinas e equipamentos para uso industrial específico não especificados anteriormente, peças e acessórios
2910701	Fabricação de automóveis, camionetas e utilitários
2910702	Fabricação de chassis com motor para automóveis, camionetas e utilitários
2910703	Fabricação de motores para automóveis, camionetas e utilitários
2920401	Fabricação de caminhões e ônibus
2920402	Fabricação de motores para caminhões e ônibus
2930101	Fabricação de cabines, carrocerias e reboques para caminhões
2930102	Fabricação de carrocerias para ônibus
2930103	Fabricação de cabines, carrocerias e reboques para outros veículos automotores, exceto caminhões e ônibus
2941700	Fabricação de peças e acessórios para o sistema motor de veículos automotores
2942500	Fabricação de peças e acessórios para os sistemas de marcha e transmissão de veículos automotores
2943300	Fabricação de peças e acessórios para o sistema de freios de veículos automotores
2944100	Fabricação de peças e acessórios para o sistema de direção e suspensão de veículos automotores
2945000	Fabricação de material elétrico e eletrônico para veículos automotores, exceto baterias
2949201	Fabricação de bancos e estofados para veículos automotores
2949299	Fabricação de outras peças e acessórios para veículos automotores não especificadas anteriormente
2950600	Recondicionamento e recuperação de motores para veículos automotores
3011301	Construção de embarcações de grande porte
3011302	Construção de embarcações para uso comercial e para usos especiais, exceto de grande porte
3012100	Construção de embarcações para esporte e lazer
3031800	Fabricação de locomotivas, vagões e outros materiais rodantes
3032600	Fabricação de peças e acessórios para veículos ferroviários
3041500	Fabricação de aeronaves
3042300	Fabricação de turbinas, motores e outros componentes e peças para aeronaves
3050400	Fabricação de veículos militares de combate
3091100	Fabricação de motocicletas, peças e acessórios
3091101	Fabricação de motocicletas
3091102	Fabricação de peças e acessórios para motocicletas
3092000	Fabricação de bicicletas e triciclos não-motorizados, peças e acessórios
3099700	Fabricação de equipamentos de transporte não especificados anteriormente
8130300	Atividades paisagísticas
3101200	Fabricação de móveis com predominância de madeira
3102100	Fabricação de móveis com predominância de metal
3103900	Fabricação de móveis de outros materiais, exceto madeira e metal
3104700	Fabricação de colchões
3211601	Lapidação de gemas
3211602	Fabricação de artefatos de joalheria e ourivesaria
3211603	Cunhagem de moedas e medalhas
3212400	Fabricação de bijuterias e artefatos semelhantes
3220500	Fabricação de instrumentos musicais, peças e acessórios
3230200	Fabricação de artefatos para pesca e esporte
3240001	Fabricação de jogos eletrônicos
3240002	Fabricação de mesas de bilhar, de sinuca e acessórios não associada à locação
3240003	Fabricação de mesas de bilhar, de sinuca e acessórios associada à locação
3240099	Fabricação de outros brinquedos e jogos recreativos não especificados anteriormente
3250701	Fabricação de instrumentos não-eletrônicos e utensílios para uso médico, cirúrgico, odontológico e de laboratório
3250702	Fabricação de mobiliário para uso médico, cirúrgico, odontológico e de laboratório
3250703	Fabricação de aparelhos e utensílios para correção de defeitos físicos e aparelhos ortopédicos em geral sob encomenda
3250704	Fabricação de aparelhos e utensílios para correção de defeitos físicos e aparelhos ortopédicos em geral, exceto sob encomenda
3250705	Fabricação de materiais para medicina e odontologia
3250706	Serviços de prótese dentária
3250707	Fabricação de artigos ópticos
3250708	Fabricação de artefatos de tecido não tecido para uso odonto-médico-hospitalar
3250709	Serviço de laboratório óptico
3291400	Fabricação de escovas, pincéis e vassouras
3292201	Fabricação de roupas de proteção e segurança e resistentes a fogo
3292202	Fabricação de equipamentos e acessórios para segurança pessoal e profissional
3299001	Fabricação de guarda-chuvas e similares
3299002	Fabricação de canetas, lápis e outros artigos para escritório
3299003	Fabricação de letras, letreiros e placas de qualquer material, exceto luminosos
3299004	Fabricação de painéis e letreiros luminosos
3299005	Fabricação de aviamentos para costura
3299006	Fabricação de velas, inclusive decorativas
3299099	Fabricação de produtos diversos não especificados anteriormente
3311200	Manutenção e reparação de tanques, reservatórios metálicos e caldeiras, exceto para veículos
3312101	Manutenção e reparação de equipamentos transmissores de comunicação
3312102	Manutenção e reparação de aparelhos e instrumentos de medida, teste e controle
3312103	Manutenção e reparação de aparelhos eletromédicos e eletroterapêuticos e equipamentos de irradiação
3312104	Manutenção e reparação de equipamentos e instrumentos ópticos
3313901	Manutenção e reparação de geradores, transformadores e motores elétricos
3313902	Manutenção e reparação de baterias e acumuladores elétricos, exceto para veículos
3313999	Manutenção e reparação de máquinas, aparelhos e materiais elétricos não especificados anteriormente
3314701	Manutenção e reparação de máquinas motrizes não-elétricas
3314702	Manutenção e reparação de equipamentos hidráulicos e pneumáticos, exceto válvulas
3314703	Manutenção e reparação de válvulas industriais
3314704	Manutenção e reparação de compressores
3314705	Manutenção e reparação de equipamentos de transmissão para fins industriais
3314706	Manutenção e reparação de máquinas, aparelhos e equipamentos para instalações térmicas
3314707	Manutenção e reparação de máquinas e aparelhos de refrigeração e ventilação para uso industrial e comercial
3314708	Manutenção e reparação de máquinas, equipamentos e aparelhos para transporte e elevação de cargas
3314709	Manutenção e reparação de máquinas de escrever, calcular e de outros equipamentos não-eletrônicos para escritório
3314710	Manutenção e reparação de máquinas e equipamentos para uso geral não especificados anteriormente
3314711	Manutenção e reparação de máquinas e equipamentos para agricultura e pecuária
3314712	Manutenção e reparação de tratores agrícolas
3314713	Manutenção e reparação de máquinas-ferramenta
3314714	Manutenção e reparação de máquinas e equipamentos para a prospecção e extração de petróleo
3314715	Manutenção e reparação de máquinas e equipamentos para uso na extração mineral, exceto na extração de petróleo
3314716	Manutenção e reparação de tratores, exceto agrícolas
3314717	Manutenção e reparação de máquinas e equipamentos de terraplenagem, pavimentação e construção, exceto tratores
3314718	Manutenção e reparação de máquinas para a indústria metalúrgica, exceto máquinas-ferramenta
3314719	Manutenção e reparação de máquinas e equipamentos para as indústrias de alimentos, bebidas e fumo
3314720	Manutenção e reparação de máquinas e equipamentos para a indústria têxtil, do vestuário, do couro e calçados
3314721	Manutenção e reparação de máquinas e aparelhos para a indústria de celulose, papel e papelão e artefatos
3314722	Manutenção e reparação de máquinas e aparelhos para a indústria do plástico
3314799	Manutenção e reparação de outras máquinas e equipamentos para usos industriais não especificados anteriormente
3315500	Manutenção e reparação de veículos ferroviários
3316301	Manutenção e reparação de aeronaves, exceto a manutenção na pista
3316302	Manutenção de aeronaves na pista
3317101	Manutenção e reparação de embarcações e estruturas flutuantes
3317102	Manutenção e reparação de embarcações para esporte e lazer
3319800	Manutenção e reparação de equipamentos e produtos não especificados anteriormente
3321000	Instalação de máquinas e equipamentos industriais
3329501	Serviços de montagem de móveis de qualquer material
3329599	Instalação de outros equipamentos não especificados anteriormente
3511500	Geração de energia elétrica
3511501	Geração de energia elétrica
3511502	Atividades de coordenação e controle da operação da geração e transmissão de energia elétrica
3512300	Transmissão de energia elétrica
3513100	Comércio atacadista de energia elétrica
3514000	Distribuição de energia elétrica
3520401	Produção de gás; processamento de gás natural
3520402	Distribuição de combustíveis gasosos por redes urbanas
3530100	Produção e distribuição de vapor, água quente e ar condicionado
3600601	Captação, tratamento e distribuição de água
3600602	Distribuição de água por caminhões
3701100	Gestão de redes de esgoto
3702900	Atividades relacionadas a esgoto, exceto a gestão de redes
3811400	Coleta de resíduos não-perigosos
3812200	Coleta de resíduos perigosos
3821100	Tratamento e disposição de resíduos não-perigosos
3822000	Tratamento e disposição de resíduos perigosos
3831901	Recuperação de sucatas de alumínio
3831999	Recuperação de materiais metálicos, exceto alumínio
3832700	Recuperação de materiais plásticos
3839401	Usinas de compostagem
3839499	Recuperação de materiais não especificados anteriormente
3900500	Descontaminação e outros serviços de gestão de resíduos
4110700	Incorporação de empreendimentos imobiliários
4120400	Construção de edifícios
4211101	Construção de rodovias e ferrovias
4211102	Pintura para sinalização em pistas rodoviárias e aeroportos
4212000	Construção de obras de arte especiais
4213800	Obras de urbanização - ruas, praças e calçadas
4221901	Construção de barragens e represas para geração de energia elétrica
4221902	Construção de estações e redes de distribuição de energia elétrica
4221903	Manutenção de redes de distribuição de energia elétrica
4221904	Construção de estações e redes de telecomunicações
4221905	Manutenção de estações e redes de telecomunicações
4222701	Construção de redes de abastecimento de água, coleta de esgoto e construções correlatas, exceto obras de irrigação
4222702	Obras de irrigação
4223500	Construção de redes de transportes por dutos, exceto para água e esgoto
4291000	Obras portuárias, marítimas e fluviais
4292801	Montagem de estruturas metálicas
4292802	Obras de montagem industrial
4299501	Construção de instalações esportivas e recreativas
4299599	Outras obras de engenharia civil não especificadas anteriormente
4311801	Demolição de edifícios e outras estruturas
4311802	Preparação de canteiro e limpeza de terreno
4312600	Perfurações e sondagens
4313400	Obras de terraplenagem
4319300	Serviços de preparação do terreno não especificados anteriormente
4321500	Instalação e manutenção elétrica
4322301	Instalações hidráulicas, sanitárias e de gás
4322302	Instalação e manutenção de sistemas centrais de ar condicionado, de ventilação e refrigeração
4322303	Instalações de sistema de prevenção contra incêndio
4329101	Instalação de painéis publicitários
4329102	Instalação de equipamentos para orientação à navegação marítima fluvial e lacustre
4329103	Instalação, manutenção e reparação de elevadores, escadas e esteiras rolantes
4329104	Montagem e instalação de sistemas e equipamentos de iluminação e sinalização em vias públicas, portos e aeroportos
4329105	Tratamentos térmicos, acústicos ou de vibração
4329199	Outras obras de instalações em construções não especificadas anteriormente
4330401	Impermeabilização em obras de engenharia civil
4330402	Instalação de portas, janelas, tetos, divisórias e armários embutidos de qualquer material
4330403	Obras de acabamento em gesso e estuque
4330404	Serviços de pintura de edifícios em geral
4330405	Aplicação de revestimentos e de resinas em interiores e exteriores
4330499	Outras obras de acabamento da construção
4391600	Obras de fundações
4399101	Administração de obras
4399102	Montagem e desmontagem de andaimes e outras estruturas temporárias
4399103	Obras de alvenaria
4399104	Serviços de operação e fornecimento de equipamentos para transporte e elevação de cargas e pessoas para uso em obras
4399105	Perfuração e construção de poços de água
4399199	Serviços especializados para construção não especificados anteriormente
4511101	Comércio a varejo de automóveis, camionetas e utilitários novos
4511102	Comércio a varejo de automóveis, camionetas e utilitários usados
4511103	Comércio por atacado de automóveis, camionetas e utilitários novos e usados
4511104	Comércio por atacado de caminhões novos e usados
4511105	Comércio por atacado de reboques e semi-reboques novos e usados
4511106	Comércio por atacado de ônibus e microônibus novos e usados
4512901	Representantes comerciais e agentes do comércio de veículos automotores
4512902	Comércio sob consignação de veículos automotores
4520001	Serviços de manutenção e reparação mecânica de veículos automotores
4520002	Serviços de lanternagem ou funilaria e pintura de veículos automotores
4520003	Serviços de manutenção e reparação elétrica de veículos automotores
4520004	Serviços de alinhamento e balanceamento de veículos automotores
4520005	Serviços de lavagem, lubrificação e polimento de veículos automotores
4520006	Serviços de borracharia para veículos automotores
4520007	Serviços de instalação, manutenção e reparação de acessórios para veículos automotores
4520008	Serviços de capotaria
4530701	Comércio por atacado de peças e acessórios novos para veículos automotores
4530702	Comércio por atacado de pneumáticos e câmaras-de-ar
4530703	Comércio a varejo de peças e acessórios novos para veículos automotores
4530704	Comércio a varejo de peças e acessórios usados para veículos automotores
4530705	Comércio a varejo de pneumáticos e câmaras-de-ar
4530706	Representantes comerciais e agentes do comércio de peças e acessórios novos e usados para veículos automotores
4541201	Comércio por atacado de motocicletas e motonetas
4541202	Comércio por atacado de peças e acessórios para motocicletas e motonetas
4541203	Comércio a varejo de motocicletas e motonetas novas
4541204	Comércio a varejo de motocicletas e motonetas usadas
4541205	Comércio a varejo de peças e acessórios para motocicletas e motonetas
4541206	Comércio a varejo de peças e acessórios novos para  motocicletas e motonetas
4541207	Comércio a varejo de peças e acessórios usados para motocicletas e motonetas
4542101	Representantes comerciais e agentes do comércio de motocicletas e motonetas, peças e acessórios
4542102	Comércio sob consignação de motocicletas e motonetas
4543900	Manutenção e reparação de motocicletas e motonetas
4611700	Representantes comerciais e agentes do comércio de matérias-primas agrícolas e animais vivos
4612500	Representantes comerciais e agentes do comércio de combustíveis, minerais, produtos siderúrgicos e químicos
4613300	Representantes comerciais e agentes do comércio de madeira, material de construção e ferragens
4614100	Representantes comerciais e agentes do comércio de máquinas, equipamentos, embarcações e aeronaves
4615000	Representantes comerciais e agentes do comércio de eletrodomésticos, móveis e artigos de uso doméstico
4616800	Representantes comerciais e agentes do comércio de têxteis, vestuário, calçados e artigos de viagem
4617600	Representantes comerciais e agentes do comércio de produtos alimentícios, bebidas e fumo
4618401	Representantes comerciais e agentes do comércio de medicamentos, cosméticos e produtos de perfumaria
4618402	Representantes comerciais e agentes do comércio de instrumentos e materiais odonto-médico-hospitalares
4618403	Representantes comerciais e agentes do comércio de jornais, revistas e outras publicações
4618499	Outros representantes comerciais e agentes do comércio especializado em produtos não especificados anteriormente
4619200	Representantes comerciais e agentes do comércio de mercadorias em geral não especializado
4621400	Comércio atacadista de café em grão
4622200	Comércio atacadista de soja
4623101	Comércio atacadista de animais vivos
4623102	Comércio atacadista de couros, lãs, peles e outros subprodutos não-comestíveis de origem animal
4623103	Comércio atacadista de algodão
4623104	Comércio atacadista de fumo em folha não beneficiado
4623105	Comércio atacadista de cacau
4623106	Comércio atacadista de sementes, flores, plantas e gramas
4623107	Comércio atacadista de sisal
4623108	Comércio atacadista de matérias-primas agrícolas com atividade de fracionamento e acondicionamento associada
4623109	Comércio atacadista de alimentos para animais
4623199	Comércio atacadista de matérias-primas agrícolas não especificadas anteriormente
4631100	Comércio atacadista de leite e laticínios
4632001	Comércio atacadista de cereais e leguminosas beneficiados
4632002	Comércio atacadista de farinhas, amidos e féculas
4632003	Comércio atacadista de cereais e leguminosas beneficiados, farinhas, amidos e féculas, com atividade de fracionamento e acondicionamento associada
4633801	Comércio atacadista de frutas, verduras, raízes, tubérculos, hortaliças e legumes frescos
4633802	Comércio atacadista de aves vivas e ovos
4633803	Comércio atacadista de coelhos e outros pequenos animais vivos para alimentação
4634601	Comércio atacadista de carnes bovinas e suínas e derivados
4634602	Comércio atacadista de aves abatidas e derivados
4634603	Comércio atacadista de pescados e frutos do mar
4634699	Comércio atacadista de carnes e derivados de outros animais
4635401	Comércio atacadista de água mineral
4635402	Comércio atacadista de cerveja, chope e refrigerante
4635403	Comércio atacadista de bebidas com atividade de fracionamento e acondicionamento associada
4635499	Comércio atacadista de bebidas não especificadas anteriormente
4636201	Comércio atacadista de fumo beneficiado
4636202	Comércio atacadista de cigarros, cigarrilhas e charutos
4637101	Comércio atacadista de café torrado, moído e solúvel
4637102	Comércio atacadista de açúcar
4637103	Comércio atacadista de óleos e gorduras
4637104	Comércio atacadista de pães, bolos, biscoitos e similares
4637105	Comércio atacadista de massas alimentícias
4637106	Comércio atacadista de sorvetes
4637107	Comércio atacadista de chocolates, confeitos, balas, bombons e semelhantes
4637199	Comércio atacadista especializado em outros produtos alimentícios não especificados anteriormente
4639701	Comércio atacadista de produtos alimentícios em geral
4639702	Comércio atacadista de produtos alimentícios em geral, com atividade de fracionamento e acondicionamento associada
4641901	Comércio atacadista de tecidos
4641902	Comércio atacadista de artigos de cama, mesa e banho
4641903	Comércio atacadista de artigos de armarinho
4642701	Comércio atacadista de artigos do vestuário e acessórios, exceto profissionais e de segurança
4642702	Comércio atacadista de roupas e acessórios para uso profissional e de segurança do trabalho
4643501	Comércio atacadista de calçados
4643502	Comércio atacadista de bolsas, malas e artigos de viagem
4644301	Comércio atacadista de medicamentos e drogas de uso humano
4644302	Comércio atacadista de medicamentos e drogas de uso veterinário
4645101	Comércio atacadista de instrumentos e materiais para uso médico, cirúrgico, hospitalar e de laboratórios
4645102	Comércio atacadista de próteses e artigos de ortopedia
4645103	Comércio atacadista de produtos odontológicos
4646001	Comércio atacadista de cosméticos e produtos de perfumaria
4646002	Comércio atacadista de produtos de higiene pessoal
4647801	Comércio atacadista de artigos de escritório e de papelaria
4647802	Comércio atacadista de livros, jornais e outras publicações
4649401	Comércio atacadista de equipamentos elétricos de uso pessoal e doméstico
4649402	Comércio atacadista de aparelhos eletrônicos de uso pessoal e doméstico
4649403	Comércio atacadista de bicicletas, triciclos e outros veículos recreativos
4649404	Comércio atacadista de móveis e artigos de colchoaria
4649405	Comércio atacadista de artigos de tapeçaria; persianas e cortinas
4649406	Comércio atacadista de lustres, luminárias e abajures
4649407	Comércio atacadista de filmes, CDs, DVDs, fitas e discos
4649408	Comércio atacadista de produtos de higiene, limpeza e conservação domiciliar
4649409	Comércio atacadista de produtos de higiene, limpeza e conservação domiciliar, com atividade de fracionamento e acondicionamento associada
4649410	Comércio atacadista de jóias, relógios e bijuterias, inclusive pedras preciosas e semipreciosas lapidadas
4649499	Comércio atacadista de outros equipamentos e artigos de uso pessoal e doméstico não especificados anteriormente
4651601	Comércio atacadista de equipamentos de informática
4651602	Comércio atacadista de suprimentos para informática
4652400	Comércio atacadista de componentes eletrônicos e equipamentos de telefonia e comunicação
4661300	Comércio atacadista de máquinas, aparelhos e equipamentos para uso agropecuário; partes e peças
4662100	Comércio atacadista de máquinas, equipamentos para terraplenagem, mineração e construção; partes e peças
4663000	Comércio atacadista de Máquinas e equipamentos para uso industrial; partes e peças
4664800	Comércio atacadista de máquinas, aparelhos e equipamentos para uso odonto-médico-hospitalar; partes e peças
4665600	Comércio atacadista de máquinas e equipamentos para uso comercial; partes e peças
4669901	Comércio atacadista de bombas e compressores; partes e peças
4669999	Comércio atacadista de outras máquinas e equipamentos não especificados anteriormente; partes e peças
4671100	Comércio atacadista de madeira e produtos derivados
4672900	Comércio atacadista de ferragens e ferramentas
4673700	Comércio atacadista de material elétrico
4674500	Comércio atacadista de cimento
4679601	Comércio atacadista de tintas, vernizes e similares
4679602	Comércio atacadista de mármores e granitos
4679603	Comércio atacadista de vidros, espelhos, vitrais e molduras
4679604	Comércio atacadista especializado de materiais de construção não especificados anteriormente
4679699	Comércio atacadista de materiais de construção em geral
4681801	Comércio atacadista de álcool carburante, biodiesel, gasolina e demais derivados de petróleo, exceto lubrificantes, não realizado por transportador re
4681802	Comércio atacadista de combustíveis realizado por transportador retalhista (T.R.R.)
4681803	Comércio atacadista de combustíveis de origem vegetal, exceto álcool carburante
4681804	Comércio atacadista de combustíveis de origem mineral em bruto
4681805	Comércio atacadista de lubrificantes
4682600	Comércio atacadista de gás liqüefeito de petróleo (GLP)
4683400	Comércio atacadista de defensivos agrícolas, adubos, fertilizantes e corretivos do solo
4684201	Comércio atacadista de resinas e elastômeros
4684202	Comércio atacadista de solventes
4684299	Comércio atacadista de outros produtos químicos e petroquímicos não especificados anteriormente
4685100	Comércio atacadista de produtos siderúrgicos e metalúrgicos, exceto para construção
4686901	Comércio atacadista de papel e papelão em bruto
4686902	Comércio atacadista de embalagens
4687701	Comércio atacadista de resíduos de papel e papelão
4687702	Comércio atacadista de resíduos e sucatas não-metálicos, exceto de papel e papelão
4687703	Comércio atacadista de resíduos e sucatas metálicos
4689301	Comércio atacadista de produtos da extração mineral, exceto combustíveis
4689302	Comércio atacadista de fios e fibras beneficiados
4689399	Comércio atacadista especializado em outros produtos intermediários não especificados anteriormente
4691500	Comércio atacadista de mercadorias em geral, com predominância de produtos alimentícios
4692300	Comércio atacadista de mercadorias em geral, com predominância de insumos agropecuários
4693100	Comércio atacadista de mercadorias em geral, sem predominância de alimentos ou de insumos agropecuários
4711301	Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - hipermercados
4711302	Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados
4712100	Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns
4713001	Lojas de departamentos ou magazines
4713002	Lojas de variedades, exceto lojas de departamentos ou magazines
4713003	Lojas duty free de aeroportos internacionais
4713004	Lojas de departamentos ou magazines, exceto lojas francas (Duty free)
4713005	Lojas francas (Duty free) de aeroportos, portos e em fronteiras terrestres
4721101	Padaria e confeitaria com predominância de produção própria
4721102	Padaria e confeitaria com predominância de revenda
4721103	Comércio varejista de laticínios e frios
4721104	Comércio varejista de doces, balas, bombons e semelhantes
4722901	Comércio varejista de carnes - açougues
4722902	Peixaria
4723700	Comércio varejista de bebidas
4724500	Comércio varejista de hortifrutigranjeiros
4729601	Tabacaria
4729602	Comércio varejista de mercadorias em lojas de conveniência
4729699	Comércio varejista de produtos alimentícios em geral ou especializado em produtos alimentícios não especificados anteriormente
4731800	Comércio varejista de combustíveis para veículos automotores
4732600	Comércio varejista de lubrificantes
4741500	Comércio varejista de tintas e materiais para pintura
4742300	Comércio varejista de material elétrico
4743100	Comércio varejista de vidros
4744001	Comércio varejista de ferragens e ferramentas
4744002	Comércio varejista de madeira e artefatos
4744003	Comércio varejista de materiais hidráulicos
4744004	Comércio varejista de cal, areia, pedra britada, tijolos e telhas
4744005	Comércio varejista de materiais de construção não especificados anteriormente
4744006	Comércio varejista de pedras para revestimento
4744099	Comércio varejista de materiais de construção em geral
4751200	Comércio varejista especializado de equipamentos e suprimentos de informática
4751201	Comércio varejista especializado de equipamentos e suprimentos de informática
4751202	Recarga de cartuchos para equipamentos de informática
4752100	Comércio varejista especializado de equipamentos de telefonia e comunicação
4753900	Comércio varejista especializado de eletrodomésticos e equipamentos de áudio e vídeo
4754701	Comércio varejista de móveis
4754702	Comércio varejista de artigos de colchoaria
4754703	Comércio varejista de artigos de iluminação
4755501	Comércio varejista de tecidos
4755502	Comercio varejista de artigos de armarinho
4755503	Comercio varejista de artigos de cama, mesa e banho
4756300	Comércio varejista especializado de instrumentos musicais e acessórios
4757100	Comércio varejista especializado de peças e acessórios para aparelhos eletroeletrônicos para uso doméstico, exceto informática e comunicação
4759801	Comércio varejista de artigos de tapeçaria, cortinas e persianas
4759899	Comércio varejista de outros artigos de uso pessoal e doméstico não especificados anteriormente
4761001	Comércio varejista de livros
4761002	Comércio varejista de jornais e revistas
4761003	Comércio varejista de artigos de papelaria
4762800	Comércio varejista de discos, CDs, DVDs e fitas
4763601	Comércio varejista de brinquedos e artigos recreativos
4763602	Comércio varejista de artigos esportivos
4763603	Comércio varejista de bicicletas e triciclos; peças e acessórios
4763604	Comércio varejista de artigos de caça, pesca e camping
4763605	Comércio varejista de embarcações e outros veículos recreativos; peças e acessórios
4771701	Comércio varejista de produtos farmacêuticos, sem manipulação de fórmulas
4771702	Comércio varejista de produtos farmacêuticos, com manipulação de fórmulas
4771703	Comércio varejista de produtos farmacêuticos homeopáticos
4771704	Comércio varejista de medicamentos veterinários
4772500	Comércio varejista de cosméticos, produtos de perfumaria e de higiene pessoal
4773300	Comércio varejista de artigos médicos e ortopédicos
4774100	Comércio varejista de artigos de óptica
4781400	Comércio varejista de artigos do vestuário e acessórios
4782201	Comércio varejista de calçados
4782202	Comércio varejista de artigos de viagem
4783101	Comércio varejista de artigos de joalheria
4783102	Comércio varejista de artigos de relojoaria
4784900	Comércio varejista de gás liqüefeito de petróleo (GLP)
4785701	Comércio varejista de antigüidades
4785799	Comércio varejista de outros artigos usados
4789001	Comércio varejista de suvenires, bijuterias e artesanatos
4789002	Comércio varejista de plantas e flores naturais
4789003	Comércio varejista de objetos de arte
4789004	Comércio varejista de animais vivos e de artigos e alimentos para animais de estimação
4789005	Comércio varejista de produtos saneantes domissanitários
4789006	Comércio varejista de fogos de artifício e artigos pirotécnicos
4789007	Comércio varejista de equipamentos para escritório
4789008	Comércio varejista de artigos fotográficos e para filmagem
4789009	Comércio varejista de armas e munições
4789099	Comércio varejista de outros produtos não especificados anteriormente
4911600	Transporte ferroviário de carga
4912401	Transporte ferroviário de passageiros intermunicipal e interestadual
4912402	Transporte ferroviário de passageiros municipal e em região metropolitana
4912403	Transporte metroviário
4921301	Transporte rodoviário coletivo de passageiros, com itinerário fixo, municipal
4921302	Transporte rodoviário coletivo de passageiros, com itinerário fixo, intermunicipal em região metropolitana
4922101	Transporte rodoviário coletivo de passageiros, com itinerário fixo, intermunicipal, exceto em região metropolitana
4922102	Transporte rodoviário coletivo de passageiros, com itinerário fixo, interestadual
4922103	Transporte rodoviário coletivo de passageiros, com itinerário fixo, internacional
4923001	Serviço de táxi
4923002	Serviço de transporte de passageiros - locação de automóveis com motorista
4924800	Transporte escolar
4929901	Transporte rodoviário coletivo de passageiros, sob regime de fretamento, municipal
4929902	Transporte rodoviário coletivo de passageiros, sob regime de fretamento, intermunicipal, interestadual e internacional
4929903	Organização de excursões em veículos rodoviários próprios, municipal
4929904	Organização de excursões em veículos rodoviários próprios, intermunicipal, interestadual e internacional
4929999	Outros transportes rodoviários de passageiros não especificados anteriormente
4930201	Transporte rodoviário de carga, exceto produtos perigosos e mudanças, municipal.
4930202	Transporte rodoviário de carga, exceto produtos perigosos e mudanças, intermunicipal, interestadual e internacional
4930203	Transporte rodoviário de produtos perigosos
4930204	Transporte rodoviário de mudanças
4940000	Transporte dutoviário
4950700	Trens turísticos, teleféricos e similares
5011401	Transporte marítimo de cabotagem - Carga
5011402	Transporte marítimo de cabotagem - passageiros
5012201	Transporte marítimo de longo curso - Carga
5012202	Transporte marítimo de longo curso - Passageiros
5021101	Transporte por navegação interior de carga, municipal, exceto travessia
5021102	Transporte por navegação interior de carga, intermunicipal, interestadual e internacional, exceto travessia
5022001	Transporte por navegação interior de passageiros em linhas regulares, municipal, exceto travessia
5022002	Transporte por navegação interior de passageiros em linhas regulares, intermunicipal, interestadual e internacional, exceto travessia
5030101	Navegação de apoio marítimo
5030102	Navegação de apoio portuário
5030103	Serviço de rebocadores e empurradores
5091201	Transporte por navegação de travessia, municipal
5091202	Transporte por navegação de travessia intermunicipal, interestadual e internacional
5099801	Transporte aquaviário para passeios turísticos
5099899	Outros transportes aquaviários não especificados anteriormente
5111100	Transporte aéreo de passageiros regular
5112901	Serviço de táxi aéreo e locação de aeronaves com tripulação
5112999	Outros serviços de transporte aéreo de passageiros não-regular
5120000	Transporte aéreo de carga
5130700	Transporte espacial
5211701	Armazéns gerais - emissão de warrant
5211702	Guarda-móveis
5211799	Depósitos de mercadorias para terceiros, exceto armazéns gerais e guarda-móveis
5212500	Carga e descarga
5221400	Concessionárias de rodovias, pontes, túneis e serviços relacionados
5222200	Terminais rodoviários e ferroviários
5223100	Estacionamento de veículos
5229001	Serviços de apoio ao transporte por táxi, inclusive centrais de chamada
5229002	Serviços de reboque de veículos
5229099	Outras atividades auxiliares dos transportes terrestres não especificadas anteriormente
5231101	Administração da infra-estrutura portuária
5231102	Atividades do Operador Portuário
5231103	Gestão de terminais aquaviários
5232000	Atividades de agenciamento marítimo
5239700	Atividades auxiliares dos transportes aquaviários não especificadas anteriormente
5239701	Serviços de praticagem
5239799	Atividades auxiliares dos transportes aquaviários não especificadas anteriormente
5240101	Operação dos aeroportos e campos de aterrissagem
5240199	Atividades auxiliares dos transportes aéreos, exceto operação dos aeroportos e campos de aterrissagem
5250801	Comissaria de despachos
5250802	Atividades de despachantes aduaneiros
5250803	Agenciamento de cargas, exceto para o transporte marítimo
5250804	Organização logística do transporte de carga
5250805	Operador de transporte multimodal - OTM
5310501	Atividades do Correio Nacional
5310502	Atividades de franqueadas do Correio Nacional
5320201	Serviços de malote não realizados pelo Correio Nacional
5320202	Serviços de entrega rápida
5510801	Hotéis
5510802	Apart-hotéis
5510803	Motéis
5590601	Albergues, exceto assistenciais
5590602	Campings
5590603	Pensões (alojamento)
5590699	Outros alojamentos não especificados anteriormente
5611201	Restaurantes e similares
5611202	Bares e outros estabelecimentos especializados em servir bebidas
5611203	Lanchonetes, casas de chá, de sucos e similares
5611204	Bares e outros estabelecimentos especializados em servir bebidas, sem entretenimento
5611205	Bares e outros estabelecimentos especializados em servir bebidas, com entretenimento
5612100	Serviços ambulantes de alimentação
5620101	Fornecimento de alimentos preparados preponderantemente para empresas
5620102	Serviços de alimentação para eventos e recepções - bufê
5620103	Cantinas - serviços de alimentação privativos
5620104	Fornecimento de alimentos preparados preponderantemente para consumo domiciliar
5811500	Edição de livros
5812300	Edição de jornais
5812301	Edição de jornais diários
5812302	Edição de jornais não diários
5813100	Edição de revistas
5819100	Edição de cadastros, listas e de outros produtos gráficos
5821200	Edição integrada à impressão de livros
5822100	Edição integrada à impressão de jornais
5822101	Edição integrada à impressão de jornais diários
5822102	Edição integrada à impressão de jornais não diários
5823900	Edição integrada à impressão de revistas
5829800	Edição integrada à impressão de cadastros, listas e de outros produtos gráficos
5911102	Produção de filmes para publicidade
5911199	Atividades de produção cinematográfica, de vídeos e de programas de televisão não especificadas anteriormente
5912001	Serviços de dublagem
5912002	Serviços de mixagem sonora em produção audiovisual
5912099	Atividades de pós-produção cinematográfica, de vídeos e de programas de televisão não especificadas anteriormente
5913800	Distribuição cinematográfica, de vídeo e de programas de televisão
5914600	Atividades de exibição cinematográfica
5920100	Atividades de gravação de som e de edição de música
6010100	Atividades de rádio
6021700	Atividades de televisão aberta
6022501	Programadoras
6022502	Atividades relacionadas à televisão por assinatura, exceto programadoras
6110801	Serviços de telefonia fixa comutada - STFC
6110802	Serviços de redes de transportes de telecomunicações - SRTT
6110803	Serviços de comunicação multimídia - SCM
6110899	Serviços de telecomunicações por fio não especificados anteriormente
6120501	Telefonia móvel celular
6120502	Serviço móvel especializado - SME
6120599	Serviços de telecomunicações sem fio não especificados anteriormente
6130200	Telecomunicações por satélite
6141800	Operadoras de televisão por assinatura por cabo
6142600	Operadoras de televisão por assinatura por microondas
6143400	Operadoras de televisão por assinatura por satélite
6190601	Provedores de acesso às redes de comunicações
6190602	Provedores de voz sobre protocolo internet - VOIP
6190699	Outras atividades de telecomunicações não especificadas anteriormente
6201500	Desenvolvimento de programas de computador sob encomenda
6201501	Desenvolvimento de programas de computador sob encomenda
6201502	Web design
6202300	Desenvolvimento e licenciamento de programas de computador customizáveis
6203100	Desenvolvimento e licenciamento de programas de computador não-customizáveis
6204000	Consultoria em tecnologia da informação
6209100	Suporte técnico, manutenção e outros serviços em tecnologia da informação
6311900	Tratamento de dados, provedores de serviços de aplicação e serviços de hospedagem na internet
6319400	Portais, provedores de conteúdo e outros serviços de informação na internet
6391700	Agências de notícias
6399200	Outras atividades de prestação de serviços de informação não especificadas anteriormente
6410700	Banco Central
6421200	Bancos comerciais
6422100	Bancos múltiplos, com carteira comercial
6423900	Caixas econômicas
6424701	Bancos cooperativos
6424702	Cooperativas centrais de crédito
6424703	Cooperativas de crédito mútuo
6424704	Cooperativas de crédito rural
6431000	Bancos múltiplos, sem carteira comercial
6432800	Bancos de investimento
6433600	Bancos de desenvolvimento
6434400	Agências de fomento
6435201	Sociedades de crédito imobiliário
6435202	Associações de poupança e empréstimo
6435203	Companhias hipotecárias
6436100	Sociedades de crédito, financiamento e investimento - financeiras
6437900	Sociedades de crédito ao microempreendedor
6438701	Bancos de câmbio
6438799	Outras instituições de intermediação não-monetária não especificadas anteriormente
6440900	Arrendamento mercantil
6450600	Sociedades de capitalização
6461100	Holdings de instituições financeiras
6462000	Holdings de instituições não-financeiras
6463800	Outras sociedades de participação, exceto holdings
6470101	Fundos de investimento, exceto previdenciários e imobiliários
6470102	Fundos de investimento previdenciários
6470103	Fundos de investimento imobiliários
6491300	Sociedades de fomento mercantil - factoring
6492100	Securitização de créditos
6493000	Administração de consórcios para aquisição de bens e direitos
6499901	Clubes de investimento
6499902	Sociedades de investimento
6499903	Fundo garantidor de crédito
6499904	Caixas de financiamento de corporações
6499905	Concessão de crédito pelas OSCIP
6499999	Outras atividades de serviços financeiros não especificadas anteriormente
6511101	Sociedade seguradora de seguros vida
6511102	Planos de auxílio-funeral
6512000	Sociedade seguradora de seguros não vida
6520100	Sociedade seguradora de seguros saúde
6530800	Resseguros
6541300	Previdência complementar fechada
6542100	Previdência complementar aberta
6550200	Planos de saúde
6611801	Bolsa de valores
6611802	Bolsa de mercadorias
6611803	Bolsa de mercadorias e futuros
6611804	Administração de mercados de balcão organizados
6612601	Corretoras de títulos e valores mobiliários
6612602	Distribuidoras de títulos e valores mobiliários
6612603	Corretoras de câmbio
6612604	Corretoras de contratos de mercadorias
6612605	Agentes de investimentos em aplicações financeiras
6613400	Administração de cartões de crédito
6619301	Serviços de liquidação e custódia
6619302	Correspondentes de instituições financeiras
6619303	Representações de bancos estrangeiros
6619304	Caixas eletrônicos
6619305	Operadoras de cartões de débito
6619399	Outras atividades auxiliares dos serviços financeiros não especificadas anteriormente
6621501	Peritos e avaliadores de seguros
6621502	Auditoria e consultoria atuarial
6622300	Corretores e agentes de seguros, de planos de previdência complementar e de saúde
6629100	Atividades auxiliares dos seguros, da previdência complementar e dos planos de saúde não especificadas anteriormente
6630400	Atividades de administração de fundos por contrato ou comissão
6810201	Compra e venda de imóveis próprios
6810202	Aluguel de imóveis próprios
6810203	Loteamento de imóveis próprios
6821801	Corretagem na compra e venda e avaliação de imóveis
6821802	Corretagem no aluguel de imóveis
6822600	Gestão e administração da propriedade imobiliária
6911701	Serviços advocatícios
6911702	Atividades auxiliares da justiça
6911703	Agente de propriedade industrial
6912500	Cartórios
6920601	Atividades de contabilidade
6920602	Atividades de consultoria e auditoria contábil e tributária
7020400	Atividades de consultoria em gestão empresarial, exceto consultoria técnica específica
7111100	Serviços de arquitetura
7112000	Serviços de engenharia
7119701	Serviços de cartografia, topografia e geodésia
7119702	Atividades de estudos geológicos
7119703	Serviços de desenho técnico relacionados à arquitetura e engenharia
7119704	Serviços de perícia técnica relacionados à segurança do trabalho
7119799	Atividades técnicas relacionadas à engenharia e arquitetura não especificadas anteriormente
7120100	Testes e análises técnicas
7210000	Pesquisa e desenvolvimento experimental em ciências físicas e naturais
7220700	Pesquisa e desenvolvimento experimental em ciências sociais e humanas
7311400	Agências de publicidade
7312200	Agenciamento de espaços para publicidade, exceto em veículos de comunicação
7319001	Criação de estandes para feiras e exposições
7319002	Promoção de vendas
7319003	Marketing direto
7319004	Consultoria em publicidade
7319099	Outras atividades de publicidade não especificadas anteriormente
7320300	Pesquisas de mercado e de opinião pública
7410201	Design
7410202	Design de interiores
7410203	Design de produto
7410299	atividades de design não especificadas anteriormente
7420001	Atividades de produção de fotografias, exceto aérea e submarina
7420002	Atividades de produção de fotografias aéreas e submarinas
7420003	Laboratórios fotográficos
7420004	Filmagem de festas e eventos
7420005	Serviços de microfilmagem
7490101	Serviços de tradução, interpretação e similares
7490102	Escafandria e mergulho
7490103	Serviços de agronomia e de consultoria às atividades agrícolas e pecuárias
7490104	Atividades de intermediação e agenciamento de serviços e negócios em geral, exceto imobiliários
7490105	Agenciamento de profissionais para atividades esportivas, culturais e artísticas
7490199	Outras atividades profissionais, científicas e técnicas não especificadas anteriormente
7500100	Atividades veterinárias
7711000	Locação de automóveis sem condutor
7719501	Locação de embarcações sem tripulação, exceto para fins recreativos
7719502	Locação de aeronaves sem tripulação
7719599	Locação de outros meios de transporte não especificados anteriormente, sem condutor
7721700	Aluguel de equipamentos recreativos e esportivos
7722500	Aluguel de fitas de vídeo, DVDs e similares
7723300	Aluguel de objetos do vestuário, jóias e acessórios
7729201	Aluguel de aparelhos de jogos eletrônicos
7729202	Aluguel de móveis, utensílios e aparelhos de uso doméstico e pessoal; instrumentos musicais
7729203	Aluguel de material médico
7729299	Aluguel de outros objetos pessoais e domésticos não especificados anteriormente
7731400	Aluguel de máquinas e equipamentos agrícolas sem operador
7732201	Aluguel de máquinas e equipamentos para construção sem operador, exceto andaimes
7732202	Aluguel de andaimes
7733100	Aluguel de máquinas e equipamentos para escritórios
7739001	Aluguel de máquinas e equipamentos para extração de minérios e petróleo, sem operador
7739002	Aluguel de equipamentos científicos, médicos e hospitalares, sem operador
7739003	Aluguel de palcos, coberturas e outras estruturas de uso temporário, exceto andaimes
7739099	Aluguel de outras máquinas e equipamentos comerciais e industriais não especificados anteriormente, sem operador
7740300	Gestão de ativos intangíveis não-financeiros
7810800	Seleção e agenciamento de mão-de-obra
7820500	Locação de mão-de-obra temporária
7830200	Fornecimento e gestão de recursos humanos para terceiros
7911200	Agências de viagens
7912100	Operadores turísticos
7990200	Serviços de reservas e outros serviços de turismo não especificados anteriormente
8011101	Atividades de vigilância e segurança privada
8011102	Serviços de adestramento de cães de guarda
8012900	Atividades de transporte de valores
8020000	Atividades de monitoramento de sistemas de segurança
8020001	Atividades de monitoramento de sistemas de segurança eletrônico
8020002	Outras atividades de serviços de segurança
8030700	Atividades de investigação particular
8111700	Serviços combinados para apoio a edifícios, exceto condomínios prediais
8112500	Condomínios prediais
8121400	Limpeza em prédios e em domicílios
8122200	Imunização e controle de pragas urbanas
8129000	Atividades de limpeza não especificadas anteriormente
8211300	Serviços combinados de escritório e apoio administrativo
8219901	Fotocópias
8219999	Preparação de documentos e serviços especializados de apoio administrativo não especificados anteriormente
8220200	Atividades de teleatendimento
8230001	Serviços de organização de feiras, congressos, exposições e festas
8230002	Casas de festas e eventos
8291100	Atividades de cobranças e informações cadastrais
8292000	Envasamento e empacotamento sob contrato
8299701	Medição de consumo de energia elétrica, gás e água
8299702	Emissão de vales-alimentação, vales-transporte e similares
8299703	Serviços de gravação de carimbos, exceto confecção
8299704	Leiloeiros independentes
8299705	Serviços de levantamento de fundos sob contrato
8299706	Casas lotéricas
8299707	Salas de acesso à internet
8299799	Outras atividades de serviços prestados principalmente às empresas não especificadas anteriormente
8411600	Administração pública em geral
8412400	Regulação das atividades de saúde, educação, serviços culturais e outros serviços sociais
8413200	Regulação das atividades econômicas
8421300	Relações exteriores
8422100	Defesa
8423000	Justiça
8424800	Segurança e ordem pública
8425600	Defesa Civil
8430200	Seguridade social obrigatória
8511200	Educação infantil - creche
8512100	Educação infantil - pré-escola
8513900	Ensino fundamental
8520100	Ensino médio
8531700	Educação superior - graduação
8532500	Educação superior - graduação e pós-graduação
8533300	Educação superior - pós-graduação e extensão
8541400	Educação profissional de nível técnico
8542200	Educação profissional de nível tecnológico
8550301	Administração de caixas escolares
8550302	Atividades de apoio à educação, exceto caixas escolares
8591100	Ensino de esportes
8592901	Ensino de dança
8592902	Ensino de artes cênicas, exceto dança
8592903	Ensino de música
8592999	Ensino de arte e cultura não especificado anteriormente
8593700	Ensino de idiomas
8599601	Formação de condutores
8599602	Cursos de pilotagem
8599603	Treinamento em informática
8599604	Treinamento em desenvolvimento profissional e gerencial
8599605	Cursos preparatórios para concursos
8599699	Outras atividades de ensino não especificadas anteriormente
8610101	Atividades de atendimento hospitalar, exceto pronto-socorro e unidades para atendimento a urgências
8610102	Atividades de atendimento em pronto-socorro e unidades hospitalares para atendimento a urgências
8621601	UTI móvel
8621602	Serviços móveis de atendimento a urgências, exceto por UTI móvel
8622400	Serviços de remoção de pacientes, exceto os serviços móveis de atendimento a urgências
8630501	Atividade médica ambulatorial com recursos para realização de procedimentos cirúrgicos
8630502	Atividade médica ambulatorial com recursos para realização de exames complementares
8630503	Atividade médica ambulatorial restrita a consultas
8630504	Atividade odontológica
8630505	Atividade odontológica sem recursos para realização de procedimentos cirúrgicos
8630506	Serviços de vacinação e imunização humana
8630507	Atividades de reprodução humana assistida
8630599	Atividades de atenção ambulatorial não especificadas anteriormente
8640201	Laboratórios de anatomia patológica e citológica
8640202	Laboratórios clínicos
8640203	Serviços de diálise e nefrologia
8640204	Serviços de tomografia
8640205	Serviços de diagnóstico por imagem com uso de radiação ionizante, exceto tomografia
8640206	Serviços de ressonância magnética
8640207	Serviços de diagnóstico por imagem sem uso de radiação ionizante, exceto ressonância magnética
8640208	Serviços de diagnóstico por registro gráfico - ECG, EEG e outros exames análogos
8640209	Serviços de diagnóstico por métodos ópticos - endoscopia e outros exames análogos
8640210	Serviços de quimioterapia
8640211	Serviços de radioterapia
8640212	Serviços de hemoterapia
8640213	Serviços de litotripcia
8640214	Serviços de bancos de células e tecidos humanos
8640299	Atividades de serviços de complementação diagnóstica e terapêutica não especificadas anteriormente
8650001	Atividades de enfermagem
8650002	Atividades de profissionais da nutrição
8650003	Atividades de psicologia e psicanálise
8650004	Atividades de fisioterapia
8650005	Atividades de terapia ocupacional
8650006	Atividades de fonoaudiologia
8650007	Atividades de terapia de nutrição enteral e parenteral
8650099	Atividades de profissionais da área de saúde não especificadas anteriormente
8660700	Atividades de apoio à gestão de saúde
8690901	Atividades de práticas integrativas e complementares em saúde humana
8690902	Atividades de banco de leite humano
8690903	Atividades de acupuntura
8690904	Atividades de podologia
8690999	Outras atividades de atenção à saúde humana não especificadas anteriormente
8711501	Clínicas e residências geriátricas
8711502	Instituições de longa permanência para idosos
8711503	Atividades de assistência a deficientes físicos, imunodeprimidos e convalescentes
8711504	Centros de apoio a pacientes com câncer e com AIDS
8711505	Condomínios residenciais para idosos e deficientes físicos
8712300	Atividades de fornecimento de infra-estrutura de apoio e assistência a paciente no domicílio
8720401	Atividades de centros de assistência psicossocial
8720499	Atividades de assistência psicossocial e à saúde a portadores de distúrbios psíquicos, deficiência mental e dependência química e grupos similares não
8730101	Orfanatos
8730102	Albergues assistenciais
8730199	Atividades de assistência social prestadas em residências coletivas e particulares não especificadas anteriormente
8800600	Serviços de assistência social sem alojamento
9001901	Produção teatral
9001902	Produção musical
9001903	Produção de espetáculos de dança
9001904	Produção de espetáculos circenses, de marionetes e similares
9001905	Produção de espetáculos de rodeios, vaquejadas e similares
9001906	Atividades de sonorização e de iluminação
9001999	Artes cênicas, espetáculos e atividades complementares não especificadas anteriormente
9002701	Atividades de artistas plásticos, jornalistas independentes e escritores
9002702	Restauração de obras-de-arte
9003500	Gestão de espaços para artes cênicas, espetáculos e outras atividades artísticas
9101500	Atividades de bibliotecas e arquivos
9102301	Atividades de museus e de exploração de lugares e prédios históricos e atrações similares
9102302	Restauração e conservação de lugares e prédios históricos
9103100	Atividades de jardins botânicos, zoológicos, parques nacionais, reservas ecológicas e áreas de proteção ambiental
9200301	Casas de bingo
9200302	Exploração de apostas em corridas de cavalos
9200399	Exploração de jogos de azar e apostas não especificados anteriormente
9311500	Gestão de instalações de esportes
9312300	Clubes sociais, esportivos e similares
9313100	Atividades de condicionamento físico
9319101	Produção e promoção de eventos esportivos
9319199	Outras atividades esportivas não especificadas anteriormente
9321200	Parques de diversão e parques temáticos
9329801	Discotecas, danceterias, salões de dança e similares
9329802	Exploração de boliches
9329803	Exploração de jogos de sinuca, bilhar e similares
9329804	Exploração de jogos eletrônicos recreativos
9329899	Outras atividades de recreação e lazer não especificadas anteriormente
9411100	Atividades de organizações associativas patronais e empresariais
9412000	Atividades de organizações associativas profissionais
9412001	Atividades de fiscalização profissional
9412099	Outras atividades associativas profissionais
9420100	Atividades de organizações sindicais
9430800	Atividades de associações de defesa de direitos sociais
9491000	Atividades de organizações religiosas ou filosóficas
9492800	Atividades de organizações políticas
9493600	Atividades de organizações associativas ligadas à cultura e à arte
9499500	Atividades associativas não especificadas anteriormente
9511800	Reparação e manutenção de computadores e de equipamentos periféricos
9512600	Reparação e manutenção de equipamentos de comunicação
9521500	Reparação e manutenção de equipamentos eletroeletrônicos de uso pessoal e doméstico
9529101	Reparação de calçados, bolsas e artigos de viagem
9529102	Chaveiros
9529103	Reparação de relógios
9529104	Reparação de bicicletas, triciclos e outros veículos não-motorizados
9529105	Reparação de artigos do mobiliário
9529106	Reparação de jóias
9529199	Reparação e manutenção de outros objetos e equipamentos pessoais e domésticos não especificados anteriormente
9601701	Lavanderias
9601702	Tinturarias
9601703	Toalheiros
9602501	Cabeleireiros, manicure e pedicure
9602502	Atividades de estética e outros serviços de cuidados com a beleza
9603301	Gestão e manutenção de cemitérios
9603302	Serviços de cremação
9603303	Serviços de sepultamento
9603304	Serviços de funerárias
9603305	Serviços de somatoconservação
9603399	Atividades funerárias e serviços relacionados não especificados anteriormente
9609201	Clinicas de estética e similares
9609202	Agências matrimoniais
9609203	Alojamento, higiene e embelezamento de animais
9609204	Exploração de máquinas de serviços pessoais acionadas por moeda
9609205	Atividades de sauna e banhos
9609206	Serviços de tatuagem e colocação de piercing
9609207	Alojamento de animais domésticos
9609208	Higiene e embelezamento de animais domésticos
9609299	Outras atividades de serviços pessoais não especificadas anteriormente
9700500	Serviços domésticos
9900800	Organismos internacionais e outras instituições extraterritoriais
8888888	Atividade Econônica não informada
\.


--
-- Data for Name: empresa; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.empresa (cnpj_basico, razao_social, natureza_juridica, qualificacao_responsavel, capital_social, porte_empresa, ente_federativo_responsavel) FROM stdin;
41273593	JULIO CESAR NUNES 39611300867	2135	50	3000.0	1	
41273594	OZINETE DELFINO CALDAS 41608224287	2135	50	5000.0	1	
41273595	GILVAN PEREIRA XAVIER 01363090380	2135	50	3000.0	1	
41273596	RODRIGO JOSE FERREIRA LOPES 05010247941	2135	50	10000.0	1	
41273597	PACHARRUS QUEIROZ DA COSTA E SILVA 03618384335	2135	50	5000.0	1	
\.


--
-- Data for Name: estabelecimento; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.estabelecimento (cnpj_basico, cnpj_ordem, cnpj_dv, identificador_matriz_filial, nome_fantasia, situacao_cadastral, data_situacao_cadastral, motivo_situacao_cadastral, nome_cidade_exterior, pais, data_inicio_atividade, cnae_fiscal_principal, cnae_fiscal_secundaria, tipo_logradouro, logradouro, numero, complemento, bairro, cep, uf, municipio, ddd_1, telefone_1, ddd_2, telefone_2, ddd_fax, fax, correio_eletronico, situacao_especial, data_situacao_especial) FROM stdin;
41273593	1	47	1	JULIO CESAR	8	20210929	1			20210318	4321500		RUA	ROMULO NALDI	01		CONJUNTO PROMORAR ESTRADA DA PARADA	02873250	SP	7107	11	22831542					JULIOCESARNUNES182@GMAIL.COM		
41273594	1	91	1		2	20210318	0			20210318	5611203	4729699	RUA	NAZARETH MESQUITA	23		PARQUE 10 DE NOVEMBRO	69054501	AM	255	92	99174383					OZINETEC70@GMAIL.COM		
41273595	1	36	1		2	20210318	0			20210318	4399103	4321500,4322301,4330404	RUA	PROFESSOR PEDRO DE MELO	545		MATAO	13401477	SP	6875	19	83436255					MARTAESS@HOTMAIL.COM		
41273596	1	80	1	NEO QUALITY AMBIENTAL SERVICOS	8	20220630	1			20210318	8599604	5819100,5811500,8599699,8599605,5813100	RUA	INCONFIDENCIA	175		CENTRO	84261610	PR	7915	42	32731238					RODRIGO_JFL@HOTMAIL.COM		
41273597	1	25	1		4	20231031	63			20210318	1096100	4789099,9329899,5620102,1033301,1031700,4729699,4721102,5229099,1099604,1094500,1091101	RUA	PALMEIRAS	1028		CAJUEIRO	65630470	MA	937	86	88694079					PACHARRUSCOSTA@GMAIL.COM		
\.


--
-- Data for Name: moti; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.moti (codigo, descricao) FROM stdin;
0	SEM MOTIVO
1	EXTINCAO POR ENCERRAMENTO LIQUIDACAO VOLUNTARIA
2	INCORPORACAO
3	FUSAO
4	CISAO TOTAL
5	ENCERRAMENTO DA FALENCIA
6	ENCERRAMENTO DA LIQUIDACAO
7	ELEVACAO A MATRIZ
8	TRANSPASSE
9	NAO INICIO DE ATIVIDADE
10	EXTINCAO PELO ENCERRAMENTO DA LIQUIDACAO JUDICIAL
11	ANULACAO POR MULTICIPLIDADE
12	ANULACAO ONLINE DE OFICIO
13	OMISSA CONTUMAZ
14	OMISSA NAO LOCALIZADA
15	INEXISTENCIA DE FATO
16	ANULACAO POR VICIOS
17	BAIXA INICIADA EM ANALISE
18	INTERRUPCAO TEMPORARIA DAS ATIVIDADES
21	PEDIDO DE BAIXA INDEFERIDA
24	POR EMISSAO CERTIDAO NEGATIVA
28	TRANSFERENCIA FILIAL CONDICAO MATRIZ
31	EXTINCAO-UNIFICACAO DA FILIAL
33	TRANSFERENCIA DO ORGAO LOCAL A CONDICAO DE FILIAL DO ORGAO REGIONAL
34	ANULACAO DE INSCRICAO INDEVIDA
35	EMPRESA ESTRANGEIRA AGUARDANDO DOCUMENTACAO
36	PRATICA IRREGULAR DE OPERACAO DE COMERCIO EXTERIOR
37	BAIXA DE PRODUTOR RURAL
38	BAIXA DEFERIDA PELA RFB AGUARDANDO ANALISE DO CONVENENTE
39	BAIXA DEFERIDA PELA RFB E INDEFERIDA PELO CONVENENTE
40	BAIXA INDEFERIDA PELA RFB E AGUARDANDO ANALISE DO CONVENENTE
41	BAIXA INDEFERIDA PELA RFB E DEFERIDA PELO CONVENENTE
42	BAIXA DEFERIDA PELA RFB E SEFIN, AGUARDANDO ANALISE SEFAZ
43	BAIXA DEFERIDA PELA RFB, AGUARDANDO ANALISE DA SEFAZ E INDEFERIDA PELA SEFIN
44	BAIXA DEFERIDA PELA RFB E SEFAZ, AGUARDANDO ANALISE SEFIN
45	BAIXA DEFERIDA PELA RFB, AGUARDANDO ANALISE DA SEFIN E INDEFERIDA PELA SEFAZ
46	BAIXA DEFERIDA PELA RFB E SEFAZ E INDEFERIDA PELA SEFIN
47	BAIXA DEFERIDA PELA RFB E SEFIN E INDEFERIDA PELA SEFAZ
48	BAIXA INDEFERIDA PELA RFB, AGARDANDO ANALISE SEFAZ E DEFERIDA PELA SEFIN
49	BAIXA INDEFERIDA PELA RFB, AGUARDANDO ANALISE DA SEFAZ E INDEFERIDA PELA SEFIN
50	BAIXA INDEFERIDA PELA RFB, DEFERIDA PELA SEFAZ E AGUARDANDO ANALISE DA SEFIN
51	BAIXA INDEFERIDA PELA RFB E SEFAZ, AGUARDANDO ANALISE DA SEFIN
52	BAIXA INDEFERIDA PELA RFB, DEFERIDA PELA SEFAZ E INDEFERIDA PELA SEFIN
53	BAIXA INDEFERIDA PELA RFB E SEFAZ E DEFERIDA PELA SEFIN
54	EXTINCAO - TRATAMENTO DIFERENCIADO DADO AS ME E EPP (LEI COMPLEMENTAR NUMERO 123/2006)
55	DEFERIDO PELO CONVENENTE, AGUARDANDO ANALISE DA RFB
60	ARTIGO 30, VI, DA IN 748/2007
61	INDICIO INTERPOS. FRAUDULENTA
62	FALTA DE PLURALIDADE DE SOCIOS
63	OMISSAO DE DECLARACOES
64	LOCALIZACAO DESCONHECIDA
66	INAPTIDAO
67	REGISTRO CANCELADO
70	ANULACAO POR NAO CONFIRMADO ATO DE REGISTRO DO MEI NA JUNTA COMERCIAL
71	INAPTIDAO (LEI 11.941/2009 ART.54)
72	DETERMINACAO JUDICIAL
73	OMISSAO CONTUMAZ
74	INCONSISTENCIA CADASTRAL
75	OBITO DO MEI - TITULAR FALECIDO
80	BAIXA REGISTRADA NA JUNTA, INDEFERIDA NA RFB
82	SUSPENSO PERANTE A COMISSAO DE VALORES MOBILIARIOS - CVM
\.


--
-- Data for Name: munic; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.munic (codigo, descricao) FROM stdin;
1	GUAJARA-MIRIM
2	ALTO ALEGRE DOS PARECIS
3	PORTO VELHO
4	BURITIS
5	JI-PARANA
6	CHUPINGUAIA
7	ARIQUEMES
8	CUJUBIM
9	CACOAL
10	NOVA UNIAO
11	PIMENTA BUENO
12	PARECIS
13	VILHENA
14	PIMENTEIRAS DO OESTE
15	JARU
16	PRIMAVERA DE RONDONIA
17	OURO PRETO DO OESTE
18	SAO FELIPE D'OESTE
19	PRESIDENTE MEDICI
20	SAO FRANCISCO DO GUAPORE
21	COSTA MARQUES
22	TEIXEIROPOLIS
23	COLORADO DO OESTE
24	VALE DO ANARI
25	ESPIGAO D'OESTE
26	AMAJARI
27	CEREJEIRAS
28	CANTA
29	ROLIM DE MOURA
30	CAROEBE
31	CALDAZINHA
32	IRACEMA
33	ALTA FLORESTA D'OESTE
34	PACARAIMA
35	ALVORADA D'OESTE
36	RORAINOPOLIS
37	CABIXI
38	UIRAMUTA
39	MACHADINHO D'OESTE
40	ANAPU
41	NOVA BRASILANDIA D'OESTE
42	BANNACH
43	SANTA LUZIA D'OESTE
44	BELTERRA
45	SAO MIGUEL DO GUAPORE
46	CACHOEIRA DO PIRIA
47	NOVA MAMORE
48	CANAA DOS CARAJAS
49	JESUPOLIS
50	CURUA
51	PROFESSOR JAMIL
52	FLORESTA DO ARAGUAIA
53	SANTO ANTONIO DE GOIAS
54	MARITUBA
55	COCALZINHO DE GOIAS
56	NOVA IPIXUNA
57	TEREZOPOLIS DE GOIAS
58	PICARRA
59	UIRAPURU
60	PLACAS
61	BURITINOPOLIS
62	QUATIPURU
63	BURITI DE GOIAS
64	SAO JOAO DA PONTA
65	GUARAITA
66	SAPUCAIA
67	VILA BOA
68	TRACUATEUA
69	INACIOLANDIA
70	VITORIA DO JARI
71	APARECIDA DO RIO DOCE
72	AGUIARNOPOLIS
73	CHAPADAO DO CEU
74	BANDEIRANTES DO TOCANTINS
75	PEROLANDIA
76	BARRA DO OURO
77	CIDADE OCIDENTAL
78	CHAPADA DE AREIA
79	MONTIVIDIU DO NORTE
80	CHAPADA DA NATIVIDADE
81	CASTELANDIA
82	CRIXAS DO TOCANTINS
83	SANTO ANTONIO DA BARRA
84	IPUEIRAS
85	ALTO HORIZONTE
86	LAVANDEIRA
87	NOVA IGUACU DE GOIAS
88	LUZINOPOLIS
89	COTRIGUACU
90	MONTE SANTO DO TOCANTINS
91	PLANALTO DA SERRA
92	OLIVEIRA DE FATIMA
93	SAO PEDRO DA CIPA
94	PUGMIL
95	PONTAL DO ARAGUAIA
96	SANTA RITA DO TOCANTINS
97	QUERENCIA
98	SANTA TEREZINHA DO TOCANTINS
99	RIBEIRAOZINHO
100	TALISMA
101	PORTO ESTRELA
102	TUPIRAMA
103	NOVA MARILANDIA
104	AGUA DOCE DO MARANHAO
105	BRASILEIA
106	ALTO ALEGRE DO MARANHAO
107	CRUZEIRO DO SUL
108	ALTO ALEGRE DO PINDARE
109	MANCIO LIMA
110	AMAPA DO MARANHAO
111	NOVA MARINGA
112	APICUM-ACU
113	FEIJO
114	ARAGUANA
115	SANTO AFONSO
116	BACABEIRA
117	NOVA BANDEIRANTES
118	BACURITUBA
119	NOVA MONTE VERDE
120	BELAGUA
121	NOVA GUARITA
122	BELA VISTA DO MARANHAO
123	SANTA CARMEM
124	BERNARDO DO MEARIM
125	TABAPORA
126	BOA VISTA DO GURUPI
127	ALTO BOA VISTA
128	BOM JESUS DAS SELVAS
129	CANABRAVA DO NORTE
130	BOM LUGAR
131	CONFRESA
132	BREJO DE AREIA
133	SAO JOSE DO XINGU
134	BURITICUPU
135	GLORIA D'OESTE
136	BURITIRANA
137	LAMBARI D'OESTE
138	CACHOEIRA GRANDE
139	RIO BRANCO
140	CAMPESTRE DO MARANHAO
141	ALCINOPOLIS
142	CAPINZAL DO NORTE
143	NOVA ALVORADA DO SUL
144	CENTRAL DO MARANHAO
145	SENA MADUREIRA
146	CENTRO DO GUILHERME
147	TARAUACA
148	CENTRO NOVO DO MARANHAO
149	XAPURI
150	CIDELANDIA
151	PLACIDO DE CASTRO
152	CONCEICAO DO LAGO-ACU
153	SENADOR GUIOMARD
154	DAVINOPOLIS
155	MANOEL URBANO
156	FEIRA NOVA DO MARANHAO
157	ASSIS BRASIL
158	FERNANDO FALCAO
159	NOVO HORIZONTE DO SUL
160	FORMOSA DA SERRA NEGRA
161	JAPORA
162	GOVERNADOR EDISON LOBAO
163	LAGUNA CARAPA
164	GOVERNADOR LUIZ ROCHA
165	ANGICO
166	GOVERNADOR NEWTON BELLO
167	ARAGOMINAS
168	GOVERNADOR NUNES FREIRE
169	ARAGUANA
170	IGARAPE DO MEIO
171	CACHOEIRINHA
172	ITAIPAVA DO GRAJAU
173	CAMPOS LINDOS
174	ITINGA DO MARANHAO
175	CARMOLANDIA
176	JATOBA
177	CARRASCO BONITO
178	JENIPAPO DOS VIEIRAS
179	DARCINOPOLIS
180	JUNCO DO MARANHAO
181	ESPERANTINA
182	LAGOA DO MATO
183	MAURILANDIA DO TOCANTINS
184	LAGO DOS RODRIGUES
185	PALMEIRAS DO TOCANTINS
186	LAGOA GRANDE DO MARANHAO
187	MURICILANDIA
188	LAJEADO NOVO
189	PALMEIRANTE
190	MARACACUME
191	PAU D'ARCO
192	MARAJA DO SENA
193	RIACHINHO
194	MARANHAOZINHO
195	SANTA FE DO ARAGUAIA
196	MATOES DO NORTE
197	SAO BENTO DO TOCANTINS
198	MILAGRES DO MARANHAO
199	SAO MIGUEL DO TOCANTINS
200	NOVA COLINAS
201	NOVO AIRAO
202	NOVA OLINDA DO MARANHAO
203	ANORI
204	OLINDA NOVA DO MARANHAO
205	ATALAIA DO NORTE
206	PAULINO NEVES
207	AUTAZES
208	PEDRO DO ROSARIO
209	BARCELOS
210	PERITORO
211	BARREIRINHA
212	PORTO RICO DO MARANHAO
213	BENJAMIN CONSTANT
214	PRESIDENTE MEDICI
215	BOCA DO ACRE
216	PRESIDENTE SARNEY
217	BORBA
218	RAPOSA
219	CANUTAMA
220	RIBAMAR FIQUENE
221	CARAUARI
222	SANTA FILOMENA DO MARANHAO
223	CAREIRO
224	SANTANA DO MARANHAO
225	COARI
226	SANTO AMARO DO MARANHAO
227	CODAJAS
228	SAO DOMINGOS DO AZEITAO
229	EIRUNEPE
230	SAO FRANCISCO DO BREJAO
231	ENVIRA
232	SAO JOAO DO CARU
233	FONTE BOA
234	SAO JOAO DO PARAISO
235	HUMAITA
236	SAO JOAO DO SOTER
237	SANTA ISABEL DO RIO NEGRO
238	SAO JOSE DOS BASILIOS
239	IPIXUNA
240	SAO PEDRO DA AGUA BRANCA
241	ITACOATIARA
242	SAO PEDRO DOS CRENTES
243	ITAPIRANGA
244	SAO RAIMUNDO DO DOCA BEZERRA
245	JAPURA
246	SAO ROBERTO
247	JURUA
248	SATUBINHA
249	JUTAI
250	SENADOR ALEXANDRE COSTA
251	LABREA
252	SENADOR LA ROCQUE
253	MANACAPURU
254	SERRANO DO MARANHAO
255	MANAUS
256	SUCUPIRA DO RIACHAO
257	MANICORE
258	TRIZIDELA DO VALE
259	MARAA
260	TUFILANDIA
261	MAUES
262	TURILANDIA
263	NHAMUNDA
264	VILA NOVA DOS MARTIRIOS
265	NOVA OLINDA DO NORTE
266	ACAUA
267	NOVO ARIPUANA
268	ALVORADA DO GURGUEIA
269	PARINTINS
270	ASSUNCAO DO PIAUI
271	PAUINI
272	BARRA D'ALCANTARA
273	SANTO ANTONIO DO ICA
274	BELA VISTA DO PIAUI
275	SAO PAULO DE OLIVENCA
276	BELEM DO PIAUI
277	SILVES
278	BETANIA DO PIAUI
279	TAPAUA
280	BOA HORA
281	TEFE
282	BOQUEIRAO DO PIAUI
283	SAO GABRIEL DA CACHOEIRA
284	BREJO DO PIAUI
285	URUCARA
286	CAJAZEIRAS DO PIAUI
287	URUCURITUBA
288	CAJUEIRO DA PRAIA
289	ALVARAES
290	CAMPO ALEGRE DO FIDALGO
291	AMATURA
292	CAMPO GRANDE DO PIAUI
293	ANAMA
294	CAMPO LARGO DO PIAUI
295	BERURI
296	CAPITAO GERVASIO OLIVEIRA
297	BOA VISTA DO RAMOS
298	CARAUBAS DO PIAUI
299	CAAPIRANGA
300	CARIDADE DO PIAUI
301	BOA VISTA
302	CAXINGO
303	CARACARAI
304	COCAL DE TELHA
305	ALTO ALEGRE
306	COCAL DOS ALVES
307	BONFIM
308	CURRAIS
309	MUCAJAI
310	CURRALINHOS
311	NORMANDIA
312	CURRAL NOVO DO PIAUI
313	SAO JOAO DA BALIZA
314	FLORESTA DO PIAUI
315	SAO LUIZ
316	FRANCISCO MACEDO
317	MATEIROS
318	GEMINIANO
320	GUARIBAS
321	NOVO JARDIM
322	ILHA GRANDE
323	RIO DA CONCEICAO
324	JATOBA DO PIAUI
325	TAIPAS DO TOCANTINS
326	JOAO COSTA
327	CARIRI DO TOCANTINS
328	JOCA MARQUES
329	JAU DO TOCANTINS
330	JUAZEIRO DO PIAUI
331	SANDOLANDIA
332	JULIO BORGES
333	SAO SALVADOR DO TOCANTINS
334	JUREMA
335	SUCUPIRA
336	LAGOINHA DO PIAUI
337	ABREULANDIA
338	LAGOA DE SAO FRANCISCO
339	BRASILANDIA DO TOCANTINS
340	LAGOA DO PIAUI
341	BOM JESUS DO TOCANTINS
342	LAGOA DO SITIO
343	CENTENARIO
344	MADEIRO
345	FORTALEZA DO TABOCAO
346	MASSAPE DO PIAUI
347	ITAPIRATINS
348	MILTON BRANDAO
349	JUARINA
350	MORRO CABECA NO TEMPO
351	LAJEADO
352	MORRO DO CHAPEU DO PIAUI
353	LAGOA DO TOCANTINS
354	MURICI DOS PORTELAS
355	PIRAQUE
356	NOSSA SENHORA DE NAZARE
357	RECURSOLANDIA
358	NOVO SANTO ANTONIO
359	RIO DOS BOIS
360	OLHO D'AGUA DO PIAUI
361	SANTA MARIA DO TOCANTINS
362	PAJEU DO PIAUI
363	SAO FELIX DO TOCANTINS
364	PAQUETA
365	TUPIRATINS
366	PAVUSSU
367	LAGOA DA CONFUSAO
368	PEDRO LAURENTINO
369	SANTA BARBARA DO PARA
370	NOVA SANTA RITA
371	SANTA LUZIA DO PARA
372	PORTO ALEGRE DO PIAUI
373	TERRA ALTA
374	RIACHO FRIO
375	ABEL FIGUEIREDO
376	RIBEIRA DO PIAUI
377	ELDORADO DOS CARAJAS
378	SANTO ANTONIO DOS MILAGRES
379	PALESTINA DO PARA
380	SAO FRANCISCO DE ASSIS DO PIAUI
381	SAO DOMINGOS DO ARAGUAIA
382	SAO GONCALO DO GURGUEIA
383	AGUA AZUL DO NORTE
384	SAO JOAO DA FRONTEIRA
385	CUMARU DO NORTE
386	SAO JOAO DA VARJOTA
387	PAU D'ARCO
388	SAO JOAO DO ARRAIAL
389	AURORA DO PARA
390	SAO LUIS DO PIAUI
391	NOVA ESPERANCA DO PIRIA
392	SAO MIGUEL DA BAIXA GRANDE
393	SAO JOAO DE PIRABAS
394	SAO MIGUEL DO FIDALGO
395	TAILANDIA
396	SEBASTIAO BARROS
397	TUCUMA
398	SEBASTIAO LEAL
399	URUARA
400	SUSSUAPARA
401	ABAETETUBA
402	TAMBORIL DO PIAUI
403	ACARA
404	TANQUE DO PIAUI
405	AFUA
406	VERA MENDES
407	ALENQUER
408	VILA NOVA DO PIAUI
409	ALMEIRIM
410	WALL FERRAZ
411	ALTAMIRA
412	BODO
413	ANAJAS
414	CAICARA DO NORTE
415	ANANINDEUA
416	FERNANDO PEDROZA
417	AUGUSTO CORREA
418	ITAJA
419	AVEIRO
420	MAJOR SALES
421	BAGRE
422	RIO DO FOGO
423	BAIAO
424	SANTA MARIA
425	BARCARENA
426	PORTO DO MANGUE
427	BELEM
428	TIBAU
429	BENEVIDES
430	SAO MIGUEL DO GOSTOSO
431	BONITO
432	SERRINHA DOS PINTOS
433	BRAGANCA
434	TENENTE LAURENTINO CRUZ
435	BREVES
436	TRIUNFO POTIGUAR
437	BUJARU
438	VENHA-VER
439	CACHOEIRA DO ARARI
440	ALCANTIL
441	CAMETA
442	ALGODAO DE JANDAIRA
443	CAPANEMA
444	AMPARO
445	CAPITAO POCO
446	APARECIDA
447	CASTANHAL
448	AREIA DE BARAUNAS
449	CHAVES
450	ASSUNCAO
451	COLARES
452	BARAUNA
453	CONCEICAO DO ARAGUAIA
454	BARRA DE SANTANA
455	CURRALINHO
456	BERNARDINO BATISTA
457	CURUCA
458	BOA VISTA
459	FARO
460	CACIMBAS
461	GURUPA
462	CAJAZEIRINHAS
463	IGARAPE-ACU
464	CAPIM
465	IGARAPE-MIRI
466	CARAUBAS
467	INHANGAPI
468	CASSERENGUE
469	IRITUIA
470	CATURITE
471	ITAITUBA
472	COXIXOLA
473	ITUPIRANGA
474	CUITE DE MAMANGUAPE
475	JACUNDA
476	CURRAL DE CIMA
477	JURUTI
478	DAMIAO
479	LIMOEIRO DO AJURU
480	GADO BRAVO
481	MAGALHAES BARATA
482	LOGRADOURO
483	MARABA
484	MARCACAO
485	MARACANA
486	MARIZOPOLIS
487	MARAPANIM
488	MATINHAS
489	MELGACO
490	MATO GROSSO
491	MOCAJUBA
492	MATUREIA
493	MOJU
494	PARARI
495	MONTE ALEGRE
496	POCO DANTAS
497	MUANA
498	POCO DE JOSE DE MOURA
499	NOVA TIMBOTEUA
500	PEDRO REGIS
501	OBIDOS
502	RIACHAO
503	OEIRAS DO PARA
504	RIACHAO DO BACAMARTE
505	ORIXIMINA
506	RIACHAO DO POCO
507	OUREM
508	RIACHO DE SANTO ANTONIO
509	PARAGOMINAS
510	SANTA CECILIA
511	PEIXE-BOI
512	SANTA INES
513	PONTA DE PEDRAS
514	JOCA CLAUDINO
515	PORTEL
516	SANTO ANDRE
517	PORTO DE MOZ
518	SAO BENTINHO
519	PRAINHA
520	SAO DOMINGOS DO CARIRI
521	PRIMAVERA
522	SAO DOMINGOS
523	SALINOPOLIS
524	SAO FRANCISCO
525	SALVATERRA
526	SAO JOSE DOS RAMOS
527	SANTA CRUZ DO ARARI
528	SAO JOSE DE PRINCESA
529	SANTA ISABEL DO PARA
530	SAO JOSE DO BREJO DO CRUZ
531	SANTA MARIA DO PARA
532	SERTAOZINHO
533	SANTANA DO ARAGUAIA
534	SOBRADO
535	SANTAREM
536	SOSSEGO
537	SANTAREM NOVO
538	TENORIO
539	SANTO ANTONIO DO TAUA
540	VIEIROPOLIS
541	SAO CAETANO DE ODIVELAS
542	ZABELE
543	SAO DOMINGOS DO CAPIM
544	ARACOIABA
545	SAO FELIX DO XINGU
546	CASINHAS
547	SAO FRANCISCO DO PARA
548	JAQUEIRA
549	SAO JOAO DO ARAGUAIA
550	JATOBA
551	SAO MIGUEL DO GUAMA
552	LAGOA GRANDE
553	SAO SEBASTIAO DA BOA VISTA
554	MANARI
555	SENADOR JOSE PORFIRIO
556	SANTA FILOMENA
557	SOURE
558	TAMANDARE
559	TOME-ACU
560	CAMPESTRE
561	TUCURUI
562	JEQUIA DA PRAIA
563	VIGIA
564	ALTO CAPARAO
565	VISEU
566	ANGELANDIA
567	REDENCAO
568	ARICANDUVA
569	RIO MARIA
570	BERIZAL
571	XINGUARA
572	BONITO DE MINAS
573	RONDON DO PARA
574	BRASILANDIA DE MINAS
575	BOM JESUS DO TOCANTINS
576	BUGRE
577	BREJO GRANDE DO ARAGUAIA
578	CABECEIRA GRANDE
579	CONCORDIA DO PARA
580	CAMPO AZUL
581	CURIONOPOLIS
582	CANTAGALO
583	DOM ELISEU
584	CATAS ALTAS
585	GARRAFAO DO NORTE
586	CATUTI
587	MAE DO RIO
588	CHAPADA GAUCHA
589	MEDICILANDIA
590	CONEGO MARINHO
591	OURILANDIA DO NORTE
592	CONFINS
593	PACAJA
594	CORREGO FUNDO
595	PARAUAPEBAS
596	CRISOLITA
597	RUROPOLIS
598	CUPARAQUE
599	SANTA MARIA DAS BARREIRAS
600	CURRAL DE DENTRO
601	AMAPA
602	DELTA
603	CALCOENE
604	DIVISA ALEGRE
605	MACAPA
606	DOM BOSCO
607	MAZAGAO
608	FRANCISCOPOLIS
609	OIAPOQUE
610	FREI LAGONEGRO
611	FERREIRA GOMES
612	FRUTA DE LEITE
613	LARANJAL DO JARI
614	GAMELEIRAS
615	SANTANA
616	GLAUCILANDIA
617	TARTARUGALZINHO
618	GOIABEIRA
619	SAO GERALDO DO ARAGUAIA
620	GOIANA
621	IPIXUNA DO PARA
622	GUARACIAMA
623	ULIANOPOLIS
624	IBIRACATU
625	BREU BRANCO
626	IMBE DE MINAS
627	GOIANESIA DO PARA
628	INDAIABIRA
629	NOVO REPARTIMENTO
630	JAPONVAR
631	JACAREACANGA
632	JENIPAPO DE MINAS
633	NOVO PROGRESSO
634	JOSE GONCALVES DE MINAS
635	TRAIRAO
636	JOSE RAYDAN
637	TERRA SANTA
638	JOSENOPOLIS
639	BRASIL NOVO
640	JUVENILIA
641	VITORIA DO XINGU
642	LEME DO PRADO
643	ACRELANDIA
644	LUISBURGO
645	BUJARI
646	LUISLANDIA
647	CAPIXABA
648	MARIO CAMPOS
649	PORTO ACRE
650	MARTINS SOARES
651	EPITACIOLANDIA
652	MIRAVANIA
653	JORDAO
654	MONTE FORMOSO
655	MARECHAL THAUMATURGO
656	NAQUE
657	PORTO WALTER
658	NATALANDIA
659	RODRIGUES ALVES
660	NINHEIRA
661	SANTA ROSA DO PURUS
662	NOVA BELEM
663	PEDRA BRANCA DO AMAPARI
664	NOVA PORTEIRINHA
665	SERRA DO NAVIO
666	NOVO ORIENTE DE MINAS
667	CUTIAS
668	NOVORIZONTE
669	ITAUBAL
670	OLHOS-D'AGUA
671	PORTO GRANDE
672	ORATORIOS
673	PRACUUBA
674	ORIZANIA
675	ALTO PARAISO
676	PADRE CARVALHO
677	CACAULANDIA
678	PAI PEDRO
679	CAMPO NOVO DE RONDONIA
680	PATIS
681	CANDEIAS DO JAMARI
682	PEDRA BONITA
683	ITAPUA DO OESTE
684	PERIQUITO
685	MONTE NEGRO
686	PIEDADE DE CARATINGA
687	RIO CRESPO
688	PINGO D'AGUA
689	NOVO HORIZONTE DO OESTE
690	PINTOPOLIS
691	CASTANHEIRAS
692	PONTO CHIQUE
693	GOVERNADOR JORGE TEIXEIRA
694	PONTO DOS VOLANTES
695	MINISTRO ANDREAZZA
696	REDUTO
697	MIRANTE DA SERRA
698	ROSARIO DA LIMEIRA
699	SERINGUEIRAS
700	SANTA BARBARA DO MONTE VERDE
701	AFONSO CUNHA
702	SANTA CRUZ DE MINAS
703	ALCANTARA
704	SANTA CRUZ DE SALINAS
705	ALDEIAS ALTAS
706	SANTA HELENA DE MINAS
707	ALTAMIRA DO MARANHAO
708	SANTO ANTONIO DO RETIRO
709	ALTO PARNAIBA
710	SAO DOMINGOS DAS DORES
711	AMARANTE DO MARANHAO
712	SAO FELIX DE MINAS
713	ANAJATUBA
714	SAO GERALDO DO BAIXIO
715	ANAPURUS
716	SAO JOAO DA LAGOA
717	ARAIOSES
718	SAO JOAO DAS MISSOES
719	ARARI
720	SAO JOAO DO PACUI
721	AXIXA
722	SAO JOAQUIM DE BICAS
723	BACABAL
724	SAO JOSE DA BARRA
725	BACURI
726	SAO SEBASTIAO DA VARGEM ALEGRE
727	BALSAS
728	SAO SEBASTIAO DO ANTA
729	BARAO DE GRAJAU
730	SARZEDO
731	BARRA DO CORDA
732	SETUBINHA
733	BARREIRINHAS
734	SEM-PEIXE
735	BENEDITO LEITE
736	SERRANOPOLIS DE MINAS
737	BEQUIMAO
738	TAPARUBA
739	BREJO
740	TOCOS DO MOJI
741	BURITI
742	UNIAO DE MINAS
743	BURITI BRAVO
744	URUANA DE MINAS
745	CAJAPIO
746	VARGEM ALEGRE
747	CAJARI
748	VARGEM GRANDE DO RIO PARDO
749	CANDIDO MENDES
750	VARJAO DE MINAS
751	CANTANHEDE
752	VERDELANDIA
753	CAROLINA
754	VEREDINHA
755	CARUTAPERA
756	VERMELHO NOVO
757	CAXIAS
758	BREJETUBA
759	CEDRAL
760	MARATAIZES
761	CHAPADINHA
762	PONTO BELO
763	CODO
764	SAO ROQUE DO CANAA
765	COELHO NETO
766	SOORETAMA
767	COLINAS
768	VILA VALERIO
769	COROATA
770	ARMACAO DOS BUZIOS
771	CURURUPU
772	CARAPEBUS
773	DOM PEDRO
774	IGUABA GRANDE
775	DUQUE BACELAR
776	MACUCO
777	ESPERANTINOPOLIS
778	PINHEIRAL
779	FORTALEZA DOS NOGUEIRAS
780	PORTO REAL
781	FORTUNA
782	SAO FRANCISCO DE ITABAPOANA
783	GODOFREDO VIANA
784	SAO JOSE DE UBA
785	GONCALVES DIAS
786	SEROPEDICA
787	GOVERNADOR ARCHER
788	TANGUA
789	GOVERNADOR EUGENIO BARROS
790	ARCO-IRIS
791	GRACA ARANHA
792	BREJO ALEGRE
793	GRAJAU
794	CANAS
795	GUIMARAES
796	FERNAO
797	HUMBERTO DE CAMPOS
798	GAVIAO PEIXOTO
799	ICATU
800	IPIGUA
801	IGARAPE GRANDE
802	JUMIRIM
803	IMPERATRIZ
804	NANTES
805	SAO LUIS GONZAGA DO MARANHAO
806	NOVA CASTILHO
807	ITAPECURU MIRIM
808	OUROESTE
809	JOAO LISBOA
810	PAULISTANIA
811	JOSELANDIA
812	PRACINHA
813	LAGO DA PEDRA
814	PRATANIA
815	LAGO DO JUNCO
816	QUADRA
817	LAGO VERDE
818	RIBEIRAO DOS INDIOS
819	LIMA CAMPOS
820	SANTA CRUZ DA ESPERANCA
821	LORETO
822	SANTA SALETE
823	LUIS DOMINGUES
824	TAQUARAL
825	MAGALHAES DE ALMEIDA
826	TRABIJU
827	MATA ROMA
828	VITORIA BRASIL
829	MATINHA
830	ARAPUA
831	MATOES
832	ARIRANHA DO IVAI
833	MIRADOR
834	BELA VISTA DA CAROBA
835	MIRINZAL
836	BOA VENTURA DE SAO ROQUE
837	MONCAO
838	BOM JESUS DO SUL
839	MONTES ALTOS
840	CAMPINA DO SIMAO
841	MORROS
842	CAMPO MAGRO
843	NINA RODRIGUES
844	CARAMBEI
845	NOVA IORQUE
846	CORONEL DOMINGOS SOARES
847	OLHO D'AGUA DAS CUNHAS
848	CRUZMALTINA
849	PACO DO LUMIAR
850	ESPERANCA NOVA
851	PALMEIRANDIA
852	ESPIGAO ALTO DO IGUACU
853	PARAIBANO
854	FERNANDES PINHEIRO
855	PARNARAMA
856	FOZ DO JORDAO
857	PASSAGEM FRANCA
858	GOIOXIM
859	PASTOS BONS
860	GUAMIRANGA
861	PEDREIRAS
862	IMBAU
863	PENALVA
864	MANFRINOPOLIS
865	PERI MIRIM
866	MARQUINHO
867	PINDARE MIRIM
868	PEROBAL
869	PINHEIRO
870	PONTAL DO PARANA
871	PIO XII
872	PORTO BARREIRO
873	PIRAPEMAS
874	PRADO FERREIRA
875	POCAO DE PEDRAS
876	QUARTO CENTENARIO
877	PORTO FRANCO
878	RESERVA DO IGUACU
879	PRESIDENTE DUTRA
880	RIO BRANCO DO IVAI
881	PRESIDENTE JUSCELINO
882	SERRANOPOLIS DO IGUACU
883	PRESIDENTE VARGAS
884	TAMARANA
885	PRIMEIRA CRUZ
886	ALTO BELA VISTA
887	RIACHAO
888	BALNEARIO ARROIO DO SILVA
889	SAO JOSE DE RIBAMAR
890	BALNEARIO GAIVOTA
891	ROSARIO
892	BANDEIRANTE
893	SAMBAIBA
894	BARRA BONITA
895	SANTA HELENA
896	BELA VISTA DO TOLDO
897	SANTA LUZIA
898	BOCAINA DO SUL
899	SANTA QUITERIA DO MARANHAO
900	BOM JESUS
901	SANTA RITA
902	BOM JESUS DO OESTE
903	SANTO ANTONIO DOS LOPES
904	BRUNOPOLIS
905	SAO BENEDITO DO RIO PRETO
906	CAPAO ALTO
907	SAO BENTO
908	CHAPADAO DO LAGEADO
909	SAO BERNARDO
910	CUNHATAI
911	SAO DOMINGOS DO MARANHAO
912	ENTRE RIOS
913	SAO FELIX DE BALSAS
914	ERMO
915	SAO FRANCISCO DO MARANHAO
916	FLOR DO SERTAO
917	SAO JOAO BATISTA
918	FREI ROGERIO
919	SAO JOAO DOS PATOS
920	IBIAM
921	SAO LUIS
922	IOMERE
923	SAO MATEUS DO MARANHAO
924	JUPIA
925	SAO RAIMUNDO DAS MANGABEIRAS
926	LUZERNA
927	SAO VICENTE FERRER
928	PAIAL
929	SITIO NOVO
930	PAINEL
931	SUCUPIRA DO NORTE
932	PALMEIRA
933	TASSO FRAGOSO
934	PRINCESA
935	TIMBIRAS
936	SALTINHO
937	TIMON
938	SANTA TEREZINHA DO PROGRESSO
939	TUNTUM
940	SANTIAGO DO SUL
941	TURIACU
942	SAO BERNARDINO
943	TUTOIA
944	SAO PEDRO DE ALCANTARA
945	URBANO SANTOS
946	TIGRINHOS
947	VARGEM GRANDE
948	TREVISO
949	VIANA
950	ZORTEA
951	VITORIA DO MEARIM
952	ARARICA
953	VITORINO FREIRE
954	BALNEARIO PINHAL
955	BOM JARDIM
956	BARRA DO QUARAI
957	SANTA INES
958	BENJAMIN CONSTANT DO SUL
959	PAULO RAMOS
960	BOA VISTA DO SUL
961	ACAILANDIA
962	CAPIVARI DO SUL
963	ESTREITO
964	CARAA
965	CAREIRO DA VARZEA
966	CERRITO
967	GUAJARA
968	CHUI
969	APUI
970	CHUVISCA
971	TEOTONIO VILELA
972	CRISTAL DO SUL
973	FORQUILHINHA
974	DILERMANDO DE AGUIAR
975	THEOBROMA
976	DOM PEDRO DE ALCANTARA
977	URUPA
978	DOUTOR RICARDO
979	VALE DO PARAISO
980	ESPERANCA DO SUL
981	CORUMBIARA
982	ESTRELA VELHA
983	CATUNDA
984	FAZENDA VILANOVA
985	JIJOCA DE JERICOACOARA
986	FLORIANO PEIXOTO
987	FORTIM
988	HERVEIRAS
989	ARARENDA
990	ITAARA
991	ITAITINGA
992	JARI
993	CHORO
994	MACAMBARA
995	COIVARAS
996	MAMPITUBA
997	JARDIM DO MULATO
998	MARQUES DE SOUZA
999	LAGOA ALEGRE
1000	MONTE ALEGRE DOS CAMPOS
1001	AGRICOLANDIA
1002	MUITOS CAPOES
1003	AGUA BRANCA
1004	NOVA CANDELARIA
1005	ALTO LONGA
1006	NOVA RAMADA
1007	ALTOS
1008	NOVO CABRAIS
1009	AMARANTE
1010	PASSA SETE
1011	ANGICAL DO PIAUI
1012	SENADOR SALGADO FILHO
1013	ANISIO DE ABREU
1014	SETE DE SETEMBRO
1015	ANTONIO ALMEIDA
1016	TABAI
1017	AROAZES
1018	TOROPI
1019	ARRAIAL
1020	TURUCU
1021	AVELINO LOPES
1022	UBIRETAMA
1023	BARRAS
1024	UNISTALDA
1025	BARREIRAS DO PIAUI
1026	VALE VERDE
1027	BARRO DURO
1028	VESPASIANO CORREA
1029	BATALHA
1030	VILA LANGARO
1031	BENEDITINOS
1032	CAMPOS DE JULIO
1033	BERTOLINIA
1034	CARLINDA
1035	BOCAINA
1036	FELIZ NATAL
1037	BOM JESUS
1038	GAUCHA DO NORTE
1039	BURITI DOS LOPES
1040	NOVA LACERDA
1041	CAMPINAS DO PIAUI
1042	NOVA UBIRATA
1043	CAMPO MAIOR
1044	NOVO MUNDO
1045	CANTO DO BURITI
1046	SAPEZAL
1047	CAPITAO DE CAMPOS
1048	UNIAO DO SUL
1049	CARACOL
1050	ABADIA DE GOIAS
1051	CASTELO DO PIAUI
1052	AGUAS LINDAS DE GOIAS
1053	COCAL
1054	AMARALINA
1055	CONCEICAO DO CANINDE
1056	BONOPOLIS
1057	CORRENTE
1058	NOVO GAMA
1059	CRISTALANDIA DO PIAUI
1060	PORTEIRAO
1061	CRISTINO CASTRO
1062	SANTA RITA DO NOVO DESTINO
1063	CURIMATA
1064	SAO PATRICIO
1065	DEMERVAL LOBAO
1066	VALPARAISO DE GOIAS
1067	DOM EXPEDITO LOPES
1068	VILA PROPICIO
1069	ELESBAO VELOSO
1070	CAMPO LIMPO DE GOIAS
1071	ELISEU MARTINS
1072	GAMELEIRA DE GOIAS
1073	ESPERANTINA
1074	IPIRANGA DE GOIAS
1075	FLORES DO PIAUI
1076	LAGOA SANTA
1077	FLORIANO
1078	BOM JESUS DO ARAGUAIA
1079	FRANCINOPOLIS
1080	COLNIZA
1081	FRANCISCO AYRES
1082	CONQUISTA D'OESTE
1083	FRANCISCO SANTOS
1084	CURVELANDIA
1085	FRONTEIRAS
1086	NOVA NAZARE
1087	GILBUES
1088	NOVA SANTA HELENA
1089	GUADALUPE
1090	NOVO SANTO ANTONIO
1091	HUGO NAPOLEAO
1092	RONDOLANDIA
1093	INHUMA
1094	SANTA CRUZ DO XINGU
1095	IPIRANGA DO PIAUI
1096	SANTA RITA DO TRIVELATO
1097	ISAIAS COELHO
1098	SANTO ANTONIO DO LESTE
1099	ITAINOPOLIS
1100	SERRA NOVA DOURADA
1101	ITAUEIRA
1102	VALE DE SAO DOMINGOS
1103	JAICOS
1104	PAU D'ARCO DO PIAUI
1105	JERUMENHA
1107	JOAQUIM PIRES
1108	JUNDIA
1109	JOSE DE FREITAS
1110	BARROCAS
1111	LANDRI SALES
1112	LUIS EDUARDO MAGALHAES
1113	LUIS CORREIA
1114	GOVERNADOR LINDENBERG
1115	LUZILANDIA
1116	MESQUITA
1117	MANOEL EMIDIO
1118	ACEGUA
1119	MARCOS PARENTE
1120	ALMIRANTE TAMANDARE DO SUL
1121	MATIAS OLIMPIO
1122	ARROIO DO PADRE
1123	MIGUEL ALVES
1124	BOA VISTA DO CADEADO
1125	MIGUEL LEAO
1126	BOA VISTA DO INCRA
1127	MONSENHOR GIL
1128	BOZANO
1129	MONSENHOR HIPOLITO
1130	CANUDOS DO VALE
1131	MONTE ALEGRE DO PIAUI
1132	CAPAO BONITO DO SUL
1133	NAZARE DO PIAUI
1134	CAPAO DO CIPO
1135	NOSSA SENHORA DOS REMEDIOS
1136	COQUEIRO BAIXO
1137	NOVO ORIENTE DO PIAUI
1138	CORONEL PILAR
1139	OEIRAS
1140	CRUZALTENSE
1141	DOMINGOS MOURAO
1142	FORQUETINHA
1143	PADRE MARCOS
1144	ITATI
1145	PAES LANDIM
1146	JACUIZINHO
1147	PALMEIRA DO PIAUI
1148	LAGOA BONITA DO SUL
1149	PALMEIRAIS
1150	MATO QUEIMADO
1151	PARNAGUA
1152	NOVO XINGU
1153	PARNAIBA
1154	PAULO BENTO
1155	PAULISTANA
1156	PEDRAS ALTAS
1157	PEDRO II
1158	PINHAL DA SERRA
1159	PICOS
1160	PINTO BANDEIRA
1161	PIMENTEIRAS
1162	QUATRO IRMAOS
1163	PIO IX
1164	ROLADOR
1165	PIRACURUCA
1166	SANTA CECILIA DO SUL
1167	PIRIPIRI
1168	SANTA MARGARIDA DO SUL
1169	PORTO
1170	SAO JOSE DO SUL
1171	PRATA DO PIAUI
1172	SAO PEDRO DAS MISSOES
1173	REDENCAO DO GURGUEIA
1174	TIO HUGO
1175	REGENERACAO
1176	WESTFALIA
1177	RIBEIRO GONCALVES
1178	FIGUEIRAO
1179	RIO GRANDE DO PIAUI
1180	NAZARIA
1181	SANTA CRUZ DO PIAUI
1183	SANTA FILOMENA
1184	IPIRANGA DO NORTE
1185	SANTA LUZ
1186	ITANHANGA
1187	SANTO ANTONIO DE LISBOA
1188	AROEIRAS DO ITAIM
1189	SANTO INACIO DO PIAUI
1190	MOJUI DOS CAMPOS
1191	SAO FELIX DO PIAUI
1192	BALNEARIO RINCAO
1193	SAO FRANCISCO DO PIAUI
1194	PESCARIA BRAVA
1195	SAO GONCALO DO PIAUI
1196	PARAISO DAS AGUAS
1197	SAO JOAO DA SERRA
1199	SAO JOAO DO PIAUI
1201	SAO JOSE DO PEIXE
1203	SAO JOSE DO PIAUI
1205	SAO JULIAO
1207	SAO MIGUEL DO TAPUIO
1209	SAO PEDRO DO PIAUI
1211	SAO RAIMUNDO NONATO
1213	SIMOES
1215	SIMPLICIO MENDES
1217	SOCORRO DO PIAUI
1219	TERESINA
1221	UNIAO
1223	URUCUI
1225	VALENCA DO PIAUI
1227	VARZEA GRANDE
1229	DIRCEU ARCOVERDE
1231	ACARAPE
1233	BANABUIU
1235	BARREIRA
1237	BARROQUINHA
1239	CHOROZINHO
1241	CROATA
1243	DEPUTADO IRAPUAN PINHEIRO
1245	ERERE
1247	EUSEBIO
1249	GRACA
1251	GUAIUBA
1253	HORIZONTE
1255	IBARETAMA
1257	IBICUITINGA
1259	IPAPORANGA
1261	MADALENA
1263	MIRAIMA
1265	OCARA
1267	PINDORETAMA
1269	PIRES FERREIRA
1271	POTIRETAMA
1273	SALITRE
1275	TARRAFAS
1277	TEJUCUOCA
1279	TURURU
1281	ARAME
1283	MIRANDA DO NORTE
1285	SANTA LUZIA DO PARUA
1287	ZE DOCA
1289	DOM INOCENCIO
1291	SAO JOAO DA CANABRAVA
1293	PASSAGEM FRANCA DO PIAUI
1295	SANTA CRUZ DOS MILAGRES
1297	BURITI DOS MONTES
1299	CABECEIRAS DO PIAUI
1301	ABAIARA
1303	ACARAU
1305	ACOPIARA
1307	AIUABA
1309	ALCANTARAS
1311	ALTANEIRA
1313	ALTO SANTO
1315	ANTONINA DO NORTE
1317	APUIARES
1319	AQUIRAZ
1321	ARACATI
1323	ARACOIABA
1325	ARARIPE
1327	ARATUBA
1329	ARNEIROZ
1331	ASSARE
1333	AURORA
1335	BAIXIO
1337	BARBALHA
1339	BARRO
1341	BATURITE
1343	BEBERIBE
1345	BELA CRUZ
1347	BOA VIAGEM
1349	BREJO SANTO
1351	CAMOCIM
1353	CAMPOS SALES
1355	CANINDE
1357	CAPISTRANO
1359	CARIDADE
1361	CARIRE
1363	CARIRIACU
1365	CARIUS
1367	CARNAUBAL
1369	CASCAVEL
1371	CATARINA
1373	CAUCAIA
1375	CEDRO
1377	CHAVAL
1379	SIGEFREDO PACHECO
1381	COREAU
1383	CRATEUS
1385	CRATO
1387	FARIAS BRITO
1389	FORTALEZA
1391	FRECHEIRINHA
1393	GENERAL SAMPAIO
1395	GRANJA
1397	GRANJEIRO
1399	GROAIRAS
1401	GUARACIABA DO NORTE
1403	GUARAMIRANGA
1405	HIDROLANDIA
1407	IBIAPINA
1409	ICO
1411	IGUATU
1413	INDEPENDENCIA
1415	IPAUMIRIM
1417	IPU
1419	IPUEIRAS
1421	IRACEMA
1423	IRAUCUBA
1425	ITAICABA
1427	ITAPAJE
1429	ITAPIPOCA
1431	ITAPIUNA
1433	ITATIRA
1435	JAGUARETAMA
1437	JAGUARIBARA
1439	JAGUARIBE
1441	JAGUARUANA
1443	JARDIM
1445	JATI
1447	JUAZEIRO DO NORTE
1449	JUCAS
1451	LAVRAS DA MANGABEIRA
1453	LIMOEIRO DO NORTE
1455	MARANGUAPE
1457	MARCO
1459	MARTINOPOLE
1461	MASSAPE
1463	MAURITI
1465	MERUOCA
1467	MILAGRES
1469	MISSAO VELHA
1471	MOMBACA
1473	MONSENHOR TABOSA
1475	MORADA NOVA
1477	MORAUJO
1479	MORRINHOS
1481	MUCAMBO
1483	MULUNGU
1485	NOVA OLINDA
1487	NOVA RUSSAS
1489	NOVO ORIENTE
1491	OROS
1493	PACAJUS
1495	PACATUBA
1497	PACOTI
1499	PACUJA
1501	PALHANO
1503	PALMACIA
1505	PARACURU
1507	PARAMBU
1509	PARAMOTI
1511	PEDRA BRANCA
1513	PENAFORTE
1515	PENTECOSTE
1517	PEREIRO
1519	PIQUET CARNEIRO
1521	PORANGA
1523	PORTEIRAS
1525	POTENGI
1527	QUIXADA
1529	QUIXERAMOBIM
1531	QUIXERE
1533	REDENCAO
1535	RERIUTABA
1537	RUSSAS
1539	SABOEIRO
1541	SANTANA DO ACARAU
1543	SANTANA DO CARIRI
1545	SANTA QUITERIA
1547	SAO BENEDITO
1549	SAO GONCALO DO AMARANTE
1551	SAO JOAO DO JAGUARIBE
1553	SAO LUIS DO CURU
1555	SENADOR POMPEU
1557	SENADOR SA
1559	SOBRAL
1561	SOLONOPOLE
1563	TABULEIRO DO NORTE
1565	TAMBORIL
1567	TAUA
1569	TIANGUA
1571	TRAIRI
1573	UBAJARA
1575	UMARI
1577	URUBURETAMA
1579	URUOCA
1581	VARZEA ALEGRE
1583	VICOSA DO CEARA
1585	MARACANAU
1587	AMONTADA
1589	CRUZ
1591	FORQUILHA
1593	ICAPUI
1595	ITAREMA
1597	MILHA
1599	PARAIPABA
1601	ACARI
1603	ASSU
1605	AFONSO BEZERRA
1607	AGUA NOVA
1609	ALEXANDRIA
1611	ALMINO AFONSO
1613	ALTO DO RODRIGUES
1615	ANGICOS
1617	ANTONIO MARTINS
1619	APODI
1621	AREIA BRANCA
1623	ARES
1625	CAMPO GRANDE
1627	BAIA FORMOSA
1629	BARCELONA
1631	BENTO FERNANDES
1633	BOM JESUS
1635	BREJINHO
1637	CAICARA DO RIO DO VENTO
1639	CAICO
1641	CAMPO REDONDO
1643	CANGUARETAMA
1645	CARAUBAS
1647	CARNAUBA DOS DANTAS
1649	CARNAUBAIS
1651	CEARA-MIRIM
1653	CERRO CORA
1655	CORONEL EZEQUIEL
1657	CORONEL JOAO PESSOA
1659	CRUZETA
1661	CURRAIS NOVOS
1663	DOUTOR SEVERIANO
1665	ENCANTO
1667	EQUADOR
1669	ESPIRITO SANTO
1671	EXTREMOZ
1673	FELIPE GUERRA
1675	FLORANIA
1677	FRANCISCO DANTAS
1679	GALINHOS
1681	GOIANINHA
1683	GOVERNADOR DIX-SEPT ROSADO
1685	GROSSOS
1687	GUAMARE
1689	IELMO MARINHO
1691	IPANGUACU
1693	IPUEIRA
1695	ITAU
1697	JACANA
1699	JANDAIRA
1701	JANDUIS
1703	BOA SAUDE
1705	JAPI
1707	JARDIM DE ANGICOS
1709	JARDIM DE PIRANHAS
1711	JARDIM DO SERIDO
1713	JOAO CAMARA
1715	JOAO DIAS
1717	JOSE DA PENHA
1719	JUCURUTU
1721	MESSIAS TARGINO
1723	LAGOA D'ANTA
1725	LAGOA DE PEDRAS
1727	LAGOA DE VELHOS
1729	LAGOA NOVA
1731	LAGOA SALGADA
1733	LAJES
1735	LAJES PINTADAS
1737	LUCRECIA
1739	LUIS GOMES
1741	MACAIBA
1743	MACAU
1745	MARCELINO VIEIRA
1747	MARTINS
1749	MAXARANGUAPE
1751	FRUTUOSO GOMES
1753	MONTANHAS
1755	MONTE ALEGRE
1757	MONTE DAS GAMELEIRAS
1759	MOSSORO
1761	NATAL
1763	NISIA FLORESTA
1765	NOVA CRUZ
1767	OLHO D'AGUA DO BORGES
1769	OURO BRANCO
1771	PARANA
1773	PARAU
1775	PARAZINHO
1777	PARELHAS
1779	PARNAMIRIM
1781	PASSA E FICA
1783	PASSAGEM
1785	PATU
1787	PAU DOS FERROS
1789	PEDRA GRANDE
1791	PEDRA PRETA
1793	PEDRO AVELINO
1795	PEDRO VELHO
1797	PENDENCIAS
1799	PILOES
1801	POCO BRANCO
1803	PORTALEGRE
1805	SERRA CAIADA
1807	PUREZA
1809	RAFAEL FERNANDES
1811	RIACHO DA CRUZ
1813	RIACHO DE SANTANA
1815	RIACHUELO
1817	RODOLFO FERNANDES
1819	RUY BARBOSA
1821	SAO FRANCISCO DO OESTE
1823	SANTA CRUZ
1825	SANTANA DO SERIDO
1827	SANTANA DO MATOS
1829	SANTO ANTONIO
1831	SAO BENTO DO NORTE
1833	SAO BENTO DO TRAIRI
1835	SAO FERNANDO
1837	SAO GONCALO DO AMARANTE
1839	SAO JOAO DO SABUGI
1841	SAO JOSE DE MIPIBU
1843	SAO JOSE DO CAMPESTRE
1845	SAO JOSE DO SERIDO
1847	SAO MIGUEL
1849	SAO PAULO DO POTENGI
1851	SAO PEDRO
1853	SAO RAFAEL
1855	SAO TOME
1857	SAO VICENTE
1859	SENADOR ELOI DE SOUZA
1861	SENADOR GEORGINO AVELINO
1863	SERRA DE SAO BENTO
1865	SERRA NEGRA DO NORTE
1867	SERRINHA
1869	SEVERIANO MELO
1871	SITIO NOVO
1873	TABOLEIRO GRANDE
1875	TAIPU
1877	TANGARA
1879	TENENTE ANANIAS
1881	TIBAU DO SUL
1883	TIMBAUBA DOS BATISTAS
1885	TOUROS
1887	UMARIZAL
1889	UPANEMA
1891	VARZEA
1893	RAFAEL GODEIRO
1895	VERA CRUZ
1897	VICOSA
1899	VILA FLOR
1901	AGUA BRANCA
1903	AGUIAR
1905	ALAGOA GRANDE
1907	ALAGOA NOVA
1909	ALAGOINHA
1911	ALHANDRA
1913	SAO JOAO DO RIO DO PEIXE
1915	ARACAGI
1917	ARARA
1919	ARARUNA
1921	AREIA
1923	AREIAL
1925	AROEIRAS
1927	SERRA DO MEL
1929	BAIA DA TRAICAO
1931	BANANEIRAS
1933	BARRA DE SANTA ROSA
1935	BARRA DE SAO MIGUEL
1937	BAYEUX
1939	BELEM
1941	BELEM DO BREJO DO CRUZ
1943	BOA VENTURA
1945	BOM JESUS
1947	BOM SUCESSO
1949	BONITO DE SANTA FE
1951	BOQUEIRAO
1953	IGARACY
1955	BORBOREMA
1957	BREJO DO CRUZ
1959	BREJO DOS SANTOS
1961	CAAPORA
1963	CABACEIRAS
1965	CABEDELO
1967	CACHOEIRA DOS INDIOS
1969	CACIMBA DE AREIA
1971	CACIMBA DE DENTRO
1973	CAICARA
1975	CAJAZEIRAS
1977	CALDAS BRANDAO
1979	CAMALAU
1981	CAMPINA GRANDE
1983	CARRAPATEIRA
1985	CATINGUEIRA
1987	CATOLE DO ROCHA
1989	CONCEICAO
1991	CONDADO
1993	CONDE
1995	CONGO
1997	COREMAS
1999	CRUZ DO ESPIRITO SANTO
2001	CUBATI
2003	CUITE
2005	CUITEGI
2007	CURRAL VELHO
2009	DESTERRO
2011	VISTA SERRANA
2013	DIAMANTE
2015	DONA INES
2017	DUAS ESTRADAS
2019	EMAS
2021	ESPERANCA
2023	FAGUNDES
2025	FREI MARTINHO
2027	GUARABIRA
2029	GURINHEM
2031	GURJAO
2033	IBIARA
2035	IMACULADA
2037	INGA
2039	ITABAIANA
2041	ITAPORANGA
2043	ITAPOROROCA
2045	ITATUBA
2047	JACARAU
2049	JERICO
2051	JOAO PESSOA
2053	JUAREZ TAVORA
2055	JUAZEIRINHO
2057	JUNCO DO SERIDO
2059	JURIPIRANGA
2061	JURU
2063	LAGOA
2065	LAGOA DE DENTRO
2067	LAGOA SECA
2069	LASTRO
2071	LIVRAMENTO
2073	LUCENA
2075	MAE D'AGUA
2077	MALTA
2079	MAMANGUAPE
2081	MANAIRA
2083	MARI
2085	MASSARANDUBA
2087	MATARACA
2089	MOGEIRO
2091	MONTADAS
2093	MONTE HOREBE
2095	MONTEIRO
2097	MULUNGU
2099	NATUBA
2101	NAZAREZINHO
2103	NOVA FLORESTA
2105	NOVA OLINDA
2107	NOVA PALMEIRA
2109	OLHO D'AGUA
2111	OLIVEDOS
2113	OURO VELHO
2115	PASSAGEM
2117	PATOS
2119	PAULISTA
2121	PEDRA BRANCA
2123	PEDRA LAVRADA
2125	PEDRAS DE FOGO
2127	PIANCO
2129	PICUI
2131	PILAR
2133	PILOES
2135	PILOEZINHOS
2137	PIRPIRITUBA
2139	PITIMBU
2141	POCINHOS
2143	POMBAL
2145	PRATA
2147	PRINCESA ISABEL
2149	PUXINANA
2151	QUEIMADAS
2153	QUIXABA
2155	REMIGIO
2157	RIACHO DOS CAVALOS
2159	RIO TINTO
2161	SALGADINHO
2163	SALGADO DE SAO FELIX
2165	SANTA CRUZ
2167	SANTA HELENA
2169	SANTA LUZIA
2171	SANTANA DE MANGUEIRA
2173	SANTANA DOS GARROTES
2175	SANTA RITA
2177	SANTA TERESINHA
2179	SAO BENTO
2181	SAO JOAO DO CARIRI
2183	SAO JOAO DO TIGRE
2185	SAO JOSE DA LAGOA TAPADA
2187	SAO JOSE DE CAIANA
2189	SAO JOSE DE ESPINHARAS
2191	SAO JOSE DE PIRANHAS
2193	SAO JOSE DO BONFIM
2195	SAO JOSE DO SABUGI
2197	SAO JOSE DOS CORDEIROS
2199	SAO MAMEDE
2201	SAO MIGUEL DE TAIPU
2203	SAO SEBASTIAO DE LAGOA DE ROCA
2205	SAO SEBASTIAO DO UMBUZEIRO
2207	SAPE
2209	SAO VICENTE DO SERIDO
2211	SERRA BRANCA
2213	SERRA DA RAIZ
2215	SERRA GRANDE
2217	SERRA REDONDA
2219	SERRARIA
2221	SOLANEA
2223	SOLEDADE
2225	SOUSA
2227	SUME
2229	TACIMA
2231	TAPEROA
2233	TAVARES
2235	TEIXEIRA
2237	TRIUNFO
2239	UIRAUNA
2241	UMBUZEIRO
2243	VARZEA
2245	BAIXA GRANDE DO RIBEIRO
2247	CANAVIEIRA
2249	COLONIA DO GURGUEIA
2251	BONFIM DO PIAUI
2253	COLONIA DO PIAUI
2255	CORONEL JOSE DIAS
2257	FARTURA DO PIAUI
2259	LAGOA DO BARRO DO PIAUI
2261	SANTA ROSA DO PIAUI
2263	SAO BRAZ DO PIAUI
2265	SAO LOURENCO DO PIAUI
2267	VARZEA BRANCA
2269	ALEGRETE DO PIAUI
2271	CALDEIRAO GRANDE DO PIAUI
2273	JACOBINA DO PIAUI
2275	MARCOLANDIA
2277	PATOS DO PIAUI
2279	QUEIMADA NOVA
2281	SANTANA DO PIAUI
2283	BRASILEIRA
2285	SAO JOSE DO DIVINO
2287	BOM PRINCIPIO DO PIAUI
2289	LAGOA DO CARRO
2291	VERTENTE DO LERIO
2293	XEXEU
2295	JUCATI
2297	SANTA CRUZ
2299	DORMENTES
2301	AFOGADOS DA INGAZEIRA
2303	AFRANIO
2305	AGRESTINA
2307	AGUA PRETA
2309	AGUAS BELAS
2311	ALAGOINHA
2313	ALIANCA
2315	ALTINHO
2317	AMARAJI
2319	ANGELIM
2321	ARARIPINA
2323	ARCOVERDE
2325	BARRA DE GUABIRABA
2327	BARREIROS
2329	BELEM DE MARIA
2331	BELEM DO SAO FRANCISCO
2333	BELO JARDIM
2335	BETANIA
2337	BEZERROS
2339	BODOCO
2341	BOM CONSELHO
2343	BOM JARDIM
2345	BONITO
2347	BREJAO
2349	BREJINHO
2351	BREJO DA MADRE DE DEUS
2353	BUENOS AIRES
2355	BUIQUE
2357	CABO DE SANTO AGOSTINHO
2359	CABROBO
2361	CACHOEIRINHA
2363	CAETES
2365	CALCADO
2367	CALUMBI
2369	CAMOCIM DE SAO FELIX
2371	CAMUTANGA
2373	CANHOTINHO
2375	CAPOEIRAS
2377	CARNAIBA
2379	CARPINA
2381	CARUARU
2383	CATENDE
2385	CEDRO
2387	CHA DE ALEGRIA
2389	CHA GRANDE
2391	CONDADO
2393	CORRENTES
2395	CORTES
2397	CUMARU
2399	CUPIRA
2401	CUSTODIA
2403	ESCADA
2405	EXU
2407	FEIRA NOVA
2409	FERREIROS
2411	FLORES
2413	FLORESTA
2415	FREI MIGUELINHO
2417	GAMELEIRA
2419	GARANHUNS
2421	GLORIA DO GOITA
2423	GOIANA
2425	GRANITO
2427	GRAVATA
2429	IATI
2431	IBIMIRIM
2433	IBIRAJUBA
2435	IGARASSU
2437	IGUARACY
2439	INAJA
2441	INGAZEIRA
2443	IPOJUCA
2445	IPUBI
2447	ITACURUBA
2449	ITAIBA
2451	ILHA DE ITAMARACA
2453	ITAPETIM
2455	ITAQUITINGA
2457	JABOATAO DOS GUARARAPES
2459	JATAUBA
2461	JOAO ALFREDO
2463	JOAQUIM NABUCO
2465	JUPI
2467	JUREMA
2469	LAGOA DE ITAENGA
2471	LAGOA DO OURO
2473	LAGOA DOS GATOS
2475	LAJEDO
2477	LIMOEIRO
2479	MACAPARANA
2481	MACHADOS
2483	MARAIAL
2485	MIRANDIBA
2487	MORENO
2489	NAZARE DA MATA
2491	OLINDA
2493	OROBO
2495	OROCO
2497	OURICURI
2499	PALMARES
2501	PALMEIRINA
2503	PANELAS
2505	PARANATAMA
2507	PARNAMIRIM
2509	PASSIRA
2511	PAUDALHO
2513	PAULISTA
2515	PEDRA
2517	PESQUEIRA
2519	PETROLANDIA
2521	PETROLINA
2523	POCAO
2525	POMBOS
2527	PRIMAVERA
2529	QUIPAPA
2531	RECIFE
2533	RIACHO DAS ALMAS
2535	RIBEIRAO
2537	RIO FORMOSO
2539	SAIRE
2541	SALGADINHO
2543	SALGUEIRO
2545	SALOA
2547	SANHARO
2549	SANTA CRUZ DO CAPIBARIBE
2551	SANTA MARIA DA BOA VISTA
2553	SANTA MARIA DO CAMBUCA
2555	SANTA TEREZINHA
2557	SAO BENEDITO DO SUL
2559	SAO BENTO DO UNA
2561	SAO CAITANO
2563	SAO JOAO
2565	SAO JOAQUIM DO MONTE
2567	SAO JOSE DA COROA GRANDE
2569	SAO JOSE DO BELMONTE
2571	SAO JOSE DO EGITO
2573	SAO LOURENCO DA MATA
2575	SAO VICENTE FERRER
2577	SERRA TALHADA
2579	SERRITA
2581	SERTANIA
2583	SIRINHAEM
2585	MOREILANDIA
2587	SOLIDAO
2589	SURUBIM
2591	TABIRA
2593	TACAIMBO
2595	TACARATU
2597	ITAMBE
2599	TAQUARITINGA DO NORTE
2601	TEREZINHA
2603	TERRA NOVA
2605	TIMBAUBA
2607	TORITAMA
2609	TRACUNHAEM
2611	TRINDADE
2613	TRIUNFO
2615	TUPANATINGA
2617	TUPARETAMA
2619	VENTUROSA
2621	VERDEJANTE
2623	VERTENTES
2625	VICENCIA
2627	VITORIA DE SANTO ANTAO
2629	CAMARAGIBE
2631	ABREU E LIMA
2633	ITAPISSUMA
2635	CARNAUBEIRA DA PENHA
2637	QUIXABA
2639	SANTA CRUZ DA BAIXA VERDE
2641	PARIPUEIRA
2643	ESTRELA DE ALAGOAS
2645	PARICONHA
2647	SANTANA DO SAO FRANCISCO
2649	SAO JOSE DA LAPA
2651	CAPITAO ANDRADE
2653	CATUJI
2655	JAMPRUCA
2657	DIVISOPOLIS
2659	MATA VERDE
2661	PALMOPOLIS
2663	ENTRE FOLHAS
2665	IPABA
2667	SANTA BARBARA DO LESTE
2669	SANTA RITA DE MINAS
2671	UBAPORANGA
2673	SANTANA DO PARAISO
2675	DURANDE
2677	SAO JOAO DO MANHUACU
2679	SAO JOAO DO MANTENINHA
2681	ALFREDO VASCONCELOS
2683	FERVEDOURO
2685	CARNEIRINHO
2687	LIMEIRA DO OESTE
2689	SENADOR AMARAL
2691	JUATUBA
2693	ICARAI DE MINAS
2695	LONTRA
2697	MONTEZUMA
2699	URUCUIA
2701	AGUA BRANCA
2703	ANADIA
2705	ARAPIRACA
2707	ATALAIA
2709	BARRA DE SANTO ANTONIO
2711	BARRA DE SAO MIGUEL
2713	BATALHA
2715	BELEM
2717	BELO MONTE
2719	BOCA DA MATA
2721	BRANQUINHA
2723	CACIMBINHAS
2725	CAJUEIRO
2727	CAMPO ALEGRE
2729	CAMPO GRANDE
2731	CANAPI
2733	CAPELA
2735	CARNEIROS
2737	CHA PRETA
2739	COITE DO NOIA
2741	COLONIA LEOPOLDINA
2743	COQUEIRO SECO
2745	CORURIPE
2747	DELMIRO GOUVEIA
2749	DOIS RIACHOS
2751	FEIRA GRANDE
2753	FELIZ DESERTO
2755	FLEXEIRAS
2757	GIRAU DO PONCIANO
2759	IBATEGUARA
2761	IGACI
2763	IGREJA NOVA
2765	INHAPI
2767	JACARE DOS HOMENS
2769	JACUIPE
2771	JAPARATINGA
2773	JARAMATAIA
2775	JOAQUIM GOMES
2777	JUNDIA
2779	JUNQUEIRO
2781	LAGOA DA CANOA
2783	LIMOEIRO DE ANADIA
2785	MACEIO
2787	MAJOR ISIDORO
2789	MARAGOGI
2791	MARAVILHA
2793	MARECHAL DEODORO
2795	MARIBONDO
2797	MAR VERMELHO
2799	MATA GRANDE
2801	MATRIZ DE CAMARAGIBE
2803	MESSIAS
2805	MINADOR DO NEGRAO
2807	MONTEIROPOLIS
2809	MURICI
2811	NOVO LINO
2813	OLHO D'AGUA DAS FLORES
2815	OLHO D'AGUA DO CASADO
2817	OLHO D'AGUA GRANDE
2819	OLIVENCA
2821	OURO BRANCO
2823	PALESTINA
2825	PALMEIRA DOS INDIOS
2827	PAO DE ACUCAR
2829	PASSO DE CAMARAGIBE
2831	PAULO JACINTO
2833	PENEDO
2835	PIACABUCU
2837	PILAR
2839	PINDOBA
2841	PIRANHAS
2843	POCO DAS TRINCHEIRAS
2845	PORTO CALVO
2847	PORTO DE PEDRAS
2849	PORTO REAL DO COLEGIO
2851	QUEBRANGULO
2853	RIO LARGO
2855	ROTEIRO
2857	SANTA LUZIA DO NORTE
2859	SANTANA DO IPANEMA
2861	SANTANA DO MUNDAU
2863	SAO BRAS
2865	SAO JOSE DA LAJE
2867	SAO JOSE DA TAPERA
2869	SAO LUIS DO QUITUNDE
2871	SAO MIGUEL DOS CAMPOS
2873	SAO MIGUEL DOS MILAGRES
2875	SAO SEBASTIAO
2877	SATUBA
2879	TANQUE D'ARCA
2881	TAQUARANA
2883	TRAIPU
2885	UNIAO DOS PALMARES
2887	VICOSA
2889	CRAIBAS
2891	SENADOR RUI PALMEIRA
2893	JAIBA
2895	MAMONAS
2897	MATIAS CARDOSO
2899	PEDRAS DE MARIA DA CRUZ
2901	RIACHINHO
2903	ARAPORA
2905	LAGOA GRANDE
2907	GUAPIMIRIM
2909	BELFORD ROXO
2911	QUEIMADOS
2913	JAPERI
2915	CARDOSO MOREIRA
2917	VARRE-SAI
2919	APERIBE
2921	RIO DAS OSTRAS
2923	QUATIS
2925	AREAL
2927	COMENDADOR LEVY GASPARIAN
2929	MARECHAL FLORIANO
2931	IRUPI
2933	SAO DOMINGOS DO NORTE
2935	VILA PAVAO
2937	LOURDES
2939	SANTO ANTONIO DO ARACANGUA
2941	SAO JOAO DE IRACEMA
2943	ILHA SOLTEIRA
2945	SUZANAPOLIS
2947	CANITAR
2949	ENGENHEIRO COELHO
2951	HORTOLANDIA
2953	HOLAMBRA
2955	TUIUTI
2957	VARGEM
2959	ESTIVA GERBI
2961	EMILIANOPOLIS
2963	PEDRINHAS PAULISTA
2965	BERTIOGA
2967	CAJATI
2969	ILHA COMPRIDA
2971	UBARANA
2973	ZACARIAS
2975	ELISIARIO
2977	MARAPOAMA
2979	NOVAIS
2981	ASPASIA
2983	MESOPOLIS
2985	NOVA CANAA PAULISTA
2987	PONTALINDA
2989	PARISI
2991	ARAPEI
2993	POTIM
2995	ALAMBARI
2997	BARRA DO CHAPEU
2999	CAMPINA DO MONTE ALEGRE
3001	FERNANDO DE NORONHA
3003	BARAUNA
3005	MUQUEM DE SAO FRANCISCO
3007	NOVA FATIMA
3009	NOVA IBIA
3011	NOVA REDENCAO
3013	NOVO HORIZONTE
3015	NOVO TRIUNFO
3017	OUROLANDIA
3019	PIRAI DO NORTE
3021	PONTO NOVO
3023	PRESIDENTE TANCREDO NEVES
3025	QUIXABEIRA
3027	RIBEIRAO DO LARGO
3029	SAO DOMINGOS
3031	SAO FELIX DO CORIBE
3033	SAO JOSE DO JACUIPE
3035	SAO JOSE DA VITORIA
3037	SAUBARA
3039	SERRA DO RAMALHO
3041	SITIO DO MATO
3043	SITIO DO QUINTO
3045	SOBRADINHO
3047	UMBURANAS
3049	VARZEDO
3051	VEREDA
3053	ITAOCA
3055	ITAPIRAPUA PAULISTA
3057	RIBEIRAO GRANDE
3059	BOM SUCESSO DE ITARARE
3061	NOVA CAMPINA
3063	TAQUARIVAI
3065	ALUMINIO
3067	ARACARIGUAMA
3069	JUSSARI
3071	AMERICA DOURADA
3073	ARATACA
3075	BARRO ALTO
3079	BURITIRAMA
3081	CAPELA DO ALTO ALEGRE
3083	CAPIM GROSSO
3085	CANUDOS
3087	DIAS D'AVILA
3089	FATIMA
3091	FILADELFIA
3093	GAVIAO
3095	GUAJERU
3097	HELIOPOLIS
3099	JOAO DOURADO
3101	AMPARO DE SAO FRANCISCO
3103	AQUIDABA
3105	ARACAJU
3107	ARAUA
3109	AREIA BRANCA
3111	BARRA DOS COQUEIROS
3113	BREJO GRANDE
3115	BOQUIM
3117	EUNAPOLIS
3119	CAMPO DO BRITO
3121	CANHOBA
3123	CANINDE DE SAO FRANCISCO
3125	CAPELA
3127	CARIRA
3129	CARMOPOLIS
3131	CEDRO DE SAO JOAO
3133	CRISTINAPOLIS
3135	NOSSA SENHORA APARECIDA
3137	CUMBE
3139	DIVINA PASTORA
3141	ESTANCIA
3143	FEIRA NOVA
3145	FREI PAULO
3147	GENERAL MAYNARD
3149	GARARU
3151	GRACCHO CARDOSO
3153	ILHA DAS FLORES
3155	INDIAROBA
3157	ITABAIANA
3159	ITABAIANINHA
3161	ITABI
3163	ITAPORANGA D'AJUDA
3165	JAPARATUBA
3167	JAPOATA
3169	LAGARTO
3171	LARANJEIRAS
3173	MACAMBIRA
3175	MALHADA DOS BOIS
3177	MALHADOR
3179	MARUIM
3181	MOITA BONITA
3183	MONTE ALEGRE DE SERGIPE
3185	MURIBECA
3187	NEOPOLIS
3189	NOSSA SENHORA DA GLORIA
3191	NOSSA SENHORA DAS DORES
3193	NOSSA SENHORA DE LOURDES
3195	NOSSA SENHORA DO SOCORRO
3197	PACATUBA
3199	PEDRA MOLE
3201	PEDRINHAS
3203	PINHAO
3205	PIRAMBU
3207	POCO REDONDO
3209	POCO VERDE
3211	PORTO DA FOLHA
3213	PROPRIA
3215	RIACHAO DO DANTAS
3217	RIACHUELO
3219	RIBEIROPOLIS
3221	ROSARIO DO CATETE
3223	SALGADO
3225	SANTA LUZIA DO ITANHY
3227	TORRE DE PEDRA
3229	SANTA ROSA DE LIMA
3231	SANTO AMARO DAS BROTAS
3233	SAO CRISTOVAO
3235	SAO DOMINGOS
3237	SAO FRANCISCO
3239	SAO MIGUEL DO ALEIXO
3241	SIMAO DIAS
3243	SIRIRI
3245	TELHA
3247	TOBIAS BARRETO
3249	TOMAR DO GERU
3251	UMBAUBA
3253	ADUSTINA
3255	ANDORINHA
3257	APUAREMA
3259	ARACAS
3261	BANZAE
3263	BOM JESUS DA SERRA
3265	BONITO
3267	CABACEIRAS DO PARAGUACU
3269	CAETANOS
3271	CARAIBAS
3273	CATURAMA
3275	FEIRA DA MATA
3277	IGRAPIUNA
3279	ITABELA
3281	ITAGUACU DA BAHIA
3283	ITATIM
3285	IUIU
3287	JUCURUCU
3289	LAGOA REAL
3291	LAJEDO DO TABOCAL
3293	MADRE DE DEUS
3295	MATINA
3297	MIRANTE
3299	MULUNGU DO MORRO
3301	ABAIRA
3303	ABARE
3305	ACAJUTIBA
3307	AGUA FRIA
3309	ERICO CARDOSO
3311	AIQUARA
3313	ALAGOINHAS
3315	ALCOBACA
3317	ALMADINA
3319	AMARGOSA
3321	AMELIA RODRIGUES
3323	ANAGE
3325	ANDARAI
3327	ANGICAL
3329	ANGUERA
3331	ANTAS
3333	ANTONIO CARDOSO
3335	ANTONIO GONCALVES
3337	APORA
3339	ARACATU
3341	ARACI
3343	ARAMARI
3345	ARATUIPE
3347	AURELINO LEAL
3349	BAIANOPOLIS
3351	BAIXA GRANDE
3353	BARRA
3355	BARRA DA ESTIVA
3357	BARRA DO CHOCA
3359	BARRA DO MENDES
3361	BARRA DO ROCHA
3363	BARREIRAS
3365	BARRO PRETO
3367	BELMONTE
3369	BELO CAMPO
3371	BIRITINGA
3373	BOA NOVA
3375	BOA VISTA DO TUPIM
3377	BOM JESUS DA LAPA
3379	BONINAL
3381	BOQUIRA
3383	BOTUPORA
3385	BREJOES
3387	BREJOLANDIA
3389	BROTAS DE MACAUBAS
3391	BRUMADO
3393	BUERAREMA
3395	CAATIBA
3397	CACHOEIRA
3399	CACULE
3401	CAEM
3403	CAETITE
3405	CAFARNAUM
3407	CAIRU
3409	CALDEIRAO GRANDE
3411	CAMACAN
3413	CAMACARI
3415	CAMAMU
3417	CAMPO ALEGRE DE LOURDES
3419	CAMPO FORMOSO
3421	CANAPOLIS
3423	CANARANA
3425	CANAVIEIRAS
3427	CANDEAL
3429	CANDEIAS
3431	CANDIBA
3433	CANDIDO SALES
3435	CANSANCAO
3437	CARAVELAS
3439	CARDEAL DA SILVA
3441	CARINHANHA
3443	CASA NOVA
3445	CASTRO ALVES
3447	CATOLANDIA
3449	CATU
3451	CENTRAL
3453	CHORROCHO
3455	CICERO DANTAS
3457	CIPO
3459	COARACI
3461	COCOS
3463	CONCEICAO DA FEIRA
3465	CONCEICAO DO ALMEIDA
3467	CONCEICAO DO COITE
3469	CONCEICAO DO JACUIPE
3471	CONDE
3473	CONDEUBA
3475	CONTENDAS DO SINCORA
3477	CORACAO DE MARIA
3479	CORDEIROS
3481	CORIBE
3483	CORONEL JOAO SA
3485	CORRENTINA
3487	COTEGIPE
3489	CRAVOLANDIA
3491	CRISOPOLIS
3493	CRISTOPOLIS
3495	CRUZ DAS ALMAS
3497	CURACA
3499	DARIO MEIRA
3501	DOM BASILIO
3503	DOM MACEDO COSTA
3505	ELISIO MEDRADO
3507	ENCRUZILHADA
3509	ENTRE RIOS
3511	ESPLANADA
3513	EUCLIDES DA CUNHA
3515	FEIRA DE SANTANA
3517	FIRMINO ALVES
3519	FLORESTA AZUL
3521	FORMOSA DO RIO PRETO
3523	GANDU
3525	GENTIO DO OURO
3527	GLORIA
3529	GONGOGI
3531	GOVERNADOR MANGABEIRA
3533	GUANAMBI
3535	GUARATINGA
3537	IACU
3539	IBIASSUCE
3541	IBICARAI
3543	IBICOARA
3545	IBICUI
3547	IBIPEBA
3549	SANTA RITA DE CASSIA
3551	IBIPITANGA
3553	IBIQUERA
3555	IBIRAPITANGA
3557	IBIRAPUA
3559	IBIRATAIA
3561	IBITIARA
3563	IBITITA
3565	IBOTIRAMA
3567	ICHU
3569	IGAPORA
3571	IGUAI
3573	ILHEUS
3575	INHAMBUPE
3577	IPECAETA
3579	IPIAU
3581	IPIRA
3583	IPUPIARA
3585	IRAJUBA
3587	IRAMAIA
3589	IRAQUARA
3591	IRARA
3593	IRECE
3595	ITABERABA
3597	ITABUNA
3599	ITACARE
3601	ITAETE
3603	ITAGI
3605	ITAGIBA
3607	ITAGIMIRIM
3609	ITAJU DO COLONIA
3611	ITAJUIPE
3613	ITAMARAJU
3615	ITAMARI
3617	ITAMBE
3619	ITANAGRA
3621	ITANHEM
3623	ITAPARICA
3625	ITAPE
3627	ITAPEBI
3629	ITAPETINGA
3631	ITAPICURU
3633	ITAPITANGA
3635	ITAQUARA
3637	ITARANTIM
3639	ITIRUCU
3641	ITIUBA
3643	ITORORO
3645	ITUACU
3647	ITUBERA
3649	JACARACI
3651	JACOBINA
3653	JAGUAQUARA
3655	JAGUARARI
3657	JAGUARIPE
3659	JANDAIRA
3661	JEQUIE
3663	JEREMOABO
3665	JIQUIRICA
3667	JITAUNA
3669	JUAZEIRO
3671	JUSSARA
3673	JUSSIAPE
3675	LAFAIETE COUTINHO
3677	LAJE
3679	LAJEDAO
3681	LAJEDINHO
3683	LAMARAO
3685	LAURO DE FREITAS
3687	LENCOIS
3689	LICINIO DE ALMEIDA
3691	LIVRAMENTO DE NOSSA SENHORA
3693	MACAJUBA
3695	MACARANI
3697	MACAUBAS
3699	MACURURE
3701	MAIQUINIQUE
3703	MAIRI
3705	MALHADA
3707	MALHADA DE PEDRAS
3709	MANOEL VITORINO
3711	MARACAS
3713	MARAGOGIPE
3715	MARAU
3717	MARCIONILIO SOUZA
3719	MASCOTE
3721	MATA DE SAO JOAO
3723	MEDEIROS NETO
3725	MIGUEL CALMON
3727	MILAGRES
3729	MIRANGABA
3731	MONTE SANTO
3733	MORPARA
3735	MORRO DO CHAPEU
3737	MORTUGABA
3739	MUCUGE
3741	MUCURI
3743	MUNDO NOVO
3745	MUNIZ FERREIRA
3747	MURITIBA
3749	MUTUIPE
3751	NAZARE
3753	NILO PECANHA
3755	NOVA CANAA
3757	NOVA ITARANA
3759	NOVA SOURE
3761	NOVA VICOSA
3763	OLINDINA
3765	OLIVEIRA DOS BREJINHOS
3767	OURICANGAS
3769	PALMAS DE MONTE ALTO
3771	PALMEIRAS
3773	PARAMIRIM
3775	PARATINGA
3777	PARIPIRANGA
3779	PAU BRASIL
3781	PAULO AFONSO
3783	PEDRAO
3785	PEDRO ALEXANDRE
3787	PIATA
3789	PILAO ARCADO
3791	PINDAI
3793	PINDOBACU
3795	PIRIPA
3797	PIRITIBA
3799	PLANALTINO
3801	PLANALTO
3803	POCOES
3805	POJUCA
3807	PORTO SEGURO
3809	POTIRAGUA
3811	PRADO
3813	PRESIDENTE DUTRA
3815	PRESIDENTE JANIO QUADROS
3817	QUEIMADAS
3819	QUIJINGUE
3821	REMANSO
3823	RETIROLANDIA
3825	RIACHAO DAS NEVES
3827	RIACHAO DO JACUIPE
3829	RIACHO DE SANTANA
3831	RIBEIRA DO AMPARO
3833	RIBEIRA DO POMBAL
3835	RIO DE CONTAS
3837	RIO DO ANTONIO
3839	RIO DO PIRES
3841	RIO REAL
3843	RODELAS
3845	RUY BARBOSA
3847	SALINAS DA MARGARIDA
3849	SALVADOR
3851	SANTA BARBARA
3853	SANTA BRIGIDA
3855	SANTA CRUZ CABRALIA
3857	SANTA CRUZ DA VITORIA
3859	SANTA INES
3861	SANTALUZ
3863	SANTA MARIA DA VITORIA
3865	SANTANA
3867	SANTANOPOLIS
3869	SANTA TERESINHA
3871	SANTO AMARO
3873	SANTO ANTONIO DE JESUS
3875	SANTO ESTEVAO
3877	SAO DESIDERIO
3879	SAO FELIX
3881	SAO FELIPE
3883	SAO FRANCISCO DO CONDE
3885	SAO GONCALO DOS CAMPOS
3887	SAO MIGUEL DAS MATAS
3889	SAO SEBASTIAO DO PASSE
3891	SAPEACU
3893	SATIRO DIAS
3895	SAUDE
3897	SEABRA
3899	SEBASTIAO LARANJEIRAS
3901	SENHOR DO BONFIM
3903	SENTO SE
3905	SERRA DOURADA
3907	SERRA PRETA
3909	SERRINHA
3911	SERROLANDIA
3913	SIMOES FILHO
3915	SOUTO SOARES
3917	TABOCAS DO BREJO VELHO
3919	TANHACU
3921	TANQUINHO
3923	TAPEROA
3925	TAPIRAMUTA
3927	TEODORO SAMPAIO
3929	TEOFILANDIA
3931	TEOLANDIA
3933	TERRA NOVA
3935	TREMEDAL
3937	TUCANO
3939	UAUA
3941	UBAIRA
3943	UBAITABA
3945	UBATA
3947	UIBAI
3949	UNA
3951	URANDI
3953	URUCUCA
3955	UTINGA
3957	VALENCA
3959	VALENTE
3961	VARZEA DO POCO
3963	VERA CRUZ
3965	VITORIA DA CONQUISTA
3967	WAGNER
3969	WENCESLAU GUIMARAES
3971	XIQUE-XIQUE
3973	LAPAO
3975	MAETINGA
3977	MANSIDAO
3979	NORDESTINA
3981	PE DE SERRA
3983	PINTADAS
3985	RAFAEL JAMBEIRO
3987	SANTA LUZIA
3989	SAO GABRIEL
3991	TANQUE NOVO
3993	TEIXEIRA DE FREITAS
3995	VARZEA NOVA
3997	VARZEA DA ROCA
3999	WANDERLEY
4001	ABADIA DOS DOURADOS
4003	ABAETE
4005	ABRE CAMPO
4007	ACAIACA
4009	ACUCENA
4011	AGUA BOA
4013	AGUA COMPRIDA
4015	AGUANIL
4017	AGUAS FORMOSAS
4019	AGUAS VERMELHAS
4021	AIMORES
4023	AIURUOCA
4025	ALAGOA
4027	ALBERTINA
4029	ALEM PARAIBA
4031	ALFENAS
4033	ALMENARA
4035	ALPERCATA
4037	ALPINOPOLIS
4039	ALTEROSA
4041	ALTO RIO DOCE
4043	ALVARENGA
4045	ALVINOPOLIS
4047	ALVORADA DE MINAS
4049	AMPARO DA SERRA
4051	ANDRADAS
4053	CACHOEIRA DE PAJEU
4055	ANDRELANDIA
4057	ANTONIO CARLOS
4059	ANTONIO DIAS
4061	ANTONIO PRADO DE MINAS
4063	ARACAI
4065	ARACITABA
4067	ARACUAI
4069	ARAGUARI
4071	ARANTINA
4073	ARAPONGA
4075	ARAPUA
4077	ARAUJOS
4079	ARAXA
4081	ARCEBURGO
4083	ARCOS
4085	AREADO
4087	ARGIRITA
4089	ARINOS
4091	ASTOLFO DUTRA
4093	ATALEIA
4095	AUGUSTO DE LIMA
4097	BAEPENDI
4099	BALDIM
4101	BAMBUI
4103	BANDEIRA
4105	BANDEIRA DO SUL
4107	BARAO DE COCAIS
4109	BARAO DO MONTE ALTO
4111	BARBACENA
4113	BARRA LONGA
4115	TRES MARIAS
4117	BARROSO
4119	BELA VISTA DE MINAS
4121	BELMIRO BRAGA
4123	BELO HORIZONTE
4125	BELO ORIENTE
4127	BELO VALE
4129	BERILO
4131	BERTOPOLIS
4133	BETIM
4135	BIAS FORTES
4137	BICAS
4139	BIQUINHAS
4141	BOA ESPERANCA
4143	BOCAINA DE MINAS
4145	BOCAIUVA
4147	BOM DESPACHO
4149	BOM JARDIM DE MINAS
4151	BOM JESUS DA PENHA
4153	BOM JESUS DO AMPARO
4155	BOM JESUS DO GALHO
4157	BOM REPOUSO
4159	BOM SUCESSO
4161	BONFIM
4163	BONFINOPOLIS DE MINAS
4165	BORDA DA MATA
4167	BOTELHOS
4169	BOTUMIRIM
4171	BRASILIA DE MINAS
4173	BRAS PIRES
4175	BRAUNAS
4177	BRASOPOLIS
4179	BRUMADINHO
4181	BUENO BRANDAO
4183	BUENOPOLIS
4185	BURITIS
4187	BURITIZEIRO
4189	CABO VERDE
4191	CACHOEIRA DA PRATA
4193	CACHOEIRA DE MINAS
4195	CACHOEIRA DOURADA
4197	CAETANOPOLIS
4199	CAETE
4201	CAIANA
4203	CAJURI
4205	CALDAS
4207	CAMACHO
4209	CAMANDUCAIA
4211	CAMBUI
4213	CAMBUQUIRA
4215	CAMPANARIO
4217	CAMPANHA
4219	CAMPESTRE
4221	CAMPINA VERDE
4223	CAMPO BELO
4225	CAMPO DO MEIO
4227	CAMPO FLORIDO
4229	CAMPOS ALTOS
4231	CAMPOS GERAIS
4233	CANAA
4235	CANAPOLIS
4237	CANA VERDE
4239	CANDEIAS
4241	CAPARAO
4243	CAPELA NOVA
4245	CAPELINHA
4247	CAPETINGA
4249	CAPIM BRANCO
4251	CAPINOPOLIS
4253	CAPITAO ENEAS
4255	CAPITOLIO
4257	CAPUTIRA
4259	CARAI
4261	CARANAIBA
4263	CARANDAI
4265	CARANGOLA
4267	CARATINGA
4269	CARBONITA
4271	CAREACU
4273	CARLOS CHAGAS
4275	CARMESIA
4277	CARMO DA CACHOEIRA
4279	CARMO DA MATA
4281	CARMO DE MINAS
4283	CARMO DO CAJURU
4285	CARMO DO PARANAIBA
4287	CARMO DO RIO CLARO
4289	CARMOPOLIS DE MINAS
4291	CARRANCAS
4293	CARVALHOPOLIS
4295	CARVALHOS
4297	CASA GRANDE
4299	CASCALHO RICO
4301	CASSIA
4303	CONCEICAO DA BARRA DE MINAS
4305	CATAGUASES
4307	CATAS ALTAS DA NORUEGA
4309	CAXAMBU
4311	CEDRO DO ABAETE
4313	CENTRAL DE MINAS
4315	CENTRALINA
4317	CHACARA
4319	CHALE
4321	CHAPADA DO NORTE
4323	CHIADOR
4325	CIPOTANEA
4327	CLARAVAL
4329	CLARO DOS POCOES
4331	CLAUDIO
4333	COIMBRA
4335	COLUNA
4337	COMENDADOR GOMES
4339	COMERCINHO
4341	CONCEICAO DA APARECIDA
4343	CONCEICAO DAS PEDRAS
4345	CONCEICAO DAS ALAGOAS
4347	CONCEICAO DE IPANEMA
4349	CONCEICAO DO MATO DENTRO
4351	CONCEICAO DO PARA
4353	CONCEICAO DO RIO VERDE
4355	CONCEICAO DOS OUROS
4357	CONGONHAL
4359	CONGONHAS
4361	CONGONHAS DO NORTE
4363	CONQUISTA
4365	CONSELHEIRO LAFAIETE
4367	CONSELHEIRO PENA
4369	CONSOLACAO
4371	CONTAGEM
4373	COQUEIRAL
4375	CORACAO DE JESUS
4377	CORDISBURGO
4379	CORDISLANDIA
4381	CORINTO
4383	COROACI
4385	COROMANDEL
4387	CORONEL FABRICIANO
4389	CORONEL MURTA
4391	CORONEL PACHECO
4393	CORONEL XAVIER CHAVES
4395	CORREGO DANTA
4397	CORREGO DO BOM JESUS
4399	CORREGO NOVO
4401	COUTO DE MAGALHAES DE MINAS
4403	CRISTAIS
4405	CRISTALIA
4407	CRISTIANO OTONI
4409	CRISTINA
4411	CRUCILANDIA
4413	CRUZEIRO DA FORTALEZA
4415	CRUZILIA
4417	CURVELO
4419	DATAS
4421	DELFIM MOREIRA
4423	DELFINOPOLIS
4425	DESCOBERTO
4427	DESTERRO DE ENTRE RIOS
4429	DESTERRO DO MELO
4431	DIAMANTINA
4433	DIOGO DE VASCONCELOS
4435	DIONISIO
4437	DIVINESIA
4439	DIVINO
4441	DIVINO DAS LARANJEIRAS
4443	DIVINOLANDIA DE MINAS
4445	DIVINOPOLIS
4447	DIVISA NOVA
4449	DOM CAVATI
4451	DOM JOAQUIM
4453	DOM SILVERIO
4455	DOM VICOSO
4457	DONA EUZEBIA
4459	DORES DE CAMPOS
4461	DORES DE GUANHAES
4463	DORES DO INDAIA
4465	DORES DO TURVO
4467	DORESOPOLIS
4469	DOURADOQUARA
4471	ELOI MENDES
4473	ENGENHEIRO CALDAS
4475	ENGENHEIRO NAVARRO
4477	ENTRE RIOS DE MINAS
4479	ERVALIA
4481	ESMERALDAS
4483	ESPERA FELIZ
4485	ESPINOSA
4487	ESPIRITO SANTO DO DOURADO
4489	ESTIVA
4491	ESTRELA DALVA
4493	ESTRELA DO INDAIA
4495	ESTRELA DO SUL
4497	EUGENOPOLIS
4499	EWBANK DA CAMARA
4501	EXTREMA
4503	FAMA
4505	FARIA LEMOS
4507	FELICIO DOS SANTOS
4509	SAO GONCALO DO RIO PRETO
4511	FELISBURGO
4513	FELIXLANDIA
4515	FERNANDES TOURINHO
4517	FERROS
4519	FLORESTAL
4521	FORMIGA
4523	FORMOSO
4525	FORTALEZA DE MINAS
4527	FORTUNA DE MINAS
4529	FRANCISCO BADARO
4531	FRANCISCO DUMONT
4533	FRANCISCO SA
4535	FREI GASPAR
4537	FREI INOCENCIO
4539	FRONTEIRA
4541	FRUTAL
4543	FUNILANDIA
4545	GALILEIA
4547	GONCALVES
4549	GONZAGA
4551	GOUVEIA
4553	GOVERNADOR VALADARES
4555	GRAO MOGOL
4557	GRUPIARA
4559	GUANHAES
4561	GUAPE
4563	GUARACIABA
4565	GUARANESIA
4567	GUARANI
4569	GUARARA
4571	GUARDA-MOR
4573	GUAXUPE
4575	GUIDOVAL
4577	GUIMARANIA
4579	GUIRICEMA
4581	GURINHATA
4583	HELIODORA
4585	IAPU
4587	IBERTIOGA
4589	IBIA
4591	IBIAI
4593	IBIRACI
4595	IBIRITE
4597	IBITIURA DE MINAS
4599	IBITURUNA
4601	IGARAPE
4603	IGARATINGA
4605	IGUATAMA
4607	IJACI
4609	ILICINEA
4611	INCONFIDENTES
4613	INDIANOPOLIS
4615	INGAI
4617	INHAPIM
4619	INHAUMA
4621	INIMUTABA
4623	IPANEMA
4625	IPATINGA
4627	IPIACU
4629	IPUIUNA
4631	IRAI DE MINAS
4633	ITABIRA
4635	ITABIRINHA
4637	ITABIRITO
4639	ITACAMBIRA
4641	ITACARAMBI
4643	ITAGUARA
4645	ITAIPE
4647	ITAJUBA
4649	ITAMARANDIBA
4651	ITAMARATI DE MINAS
4653	ITAMBACURI
4655	ITAMBE DO MATO DENTRO
4657	ITAMOGI
4659	ITAMONTE
4661	ITANHANDU
4663	ITANHOMI
4665	ITAOBIM
4667	ITAPAGIPE
4669	ITAPECERICA
4671	ITAPEVA
4673	ITATIAIUCU
4675	ITAUNA
4677	ITAVERAVA
4679	ITINGA
4681	ITUETA
4683	ITUIUTABA
4685	ITUMIRIM
4687	ITURAMA
4689	ITUTINGA
4691	JABOTICATUBAS
4693	JACINTO
4695	JACUI
4697	JACUTINGA
4699	JAGUARACU
4701	JANAUBA
4703	JANUARIA
4705	JAPARAIBA
4707	JECEABA
4709	JEQUERI
4711	JEQUITAI
4713	JEQUITIBA
4715	JEQUITINHONHA
4717	JESUANIA
4719	JOAIMA
4721	JOANESIA
4723	JOAO MONLEVADE
4725	JOAO PINHEIRO
4727	JOAQUIM FELICIO
4729	JORDANIA
4731	NOVA UNIAO
4733	JUIZ DE FORA
4735	JURAMENTO
4737	JURUAIA
4739	LADAINHA
4741	LAGAMAR
4743	LAGOA DA PRATA
4745	LAGOA DOS PATOS
4747	LAGOA DOURADA
4749	LAGOA FORMOSA
4751	LAGOA SANTA
4753	LAJINHA
4755	LAMBARI
4757	LAMIM
4759	LARANJAL
4761	LASSANCE
4763	LAVRAS
4765	LEANDRO FERREIRA
4767	LEOPOLDINA
4769	LIBERDADE
4771	LIMA DUARTE
4773	LUMINARIAS
4775	LUZ
4777	MACHACALIS
4779	MACHADO
4781	MADRE DE DEUS DE MINAS
4783	MALACACHETA
4785	MANGA
4787	MANHUACU
4789	MANHUMIRIM
4791	MANTENA
4793	MARAVILHAS
4795	MAR DE ESPANHA
4797	MARIA DA FE
4799	MARIANA
4801	MARILAC
4803	MARIPA DE MINAS
4805	MARLIERIA
4807	MARMELOPOLIS
4809	MARTINHO CAMPOS
4811	MATERLANDIA
4813	MATEUS LEME
4815	MATIAS BARBOSA
4817	MATIPO
4819	MATO VERDE
4821	MATOZINHOS
4823	MATUTINA
4825	MEDEIROS
4827	MEDINA
4829	MENDES PIMENTEL
4831	MERCES
4833	MESQUITA
4835	MINAS NOVAS
4837	MINDURI
4839	MIRABELA
4841	MIRADOURO
4843	MIRAI
4845	MOEDA
4847	MOEMA
4849	MONJOLOS
4851	MONSENHOR PAULO
4853	MONTALVANIA
4855	MONTE ALEGRE DE MINAS
4857	MONTE AZUL
4859	MONTE BELO
4861	MONTE CARMELO
4863	MONTE SANTO DE MINAS
4865	MONTES CLAROS
4867	MONTE SIAO
4869	MORADA NOVA DE MINAS
4871	MORRO DA GARCA
4873	MORRO DO PILAR
4875	MUNHOZ
4877	MURIAE
4879	MUTUM
4881	MUZAMBINHO
4883	NACIP RAYDAN
4885	NANUQUE
4887	NATERCIA
4889	NAZARENO
4891	NEPOMUCENO
4893	NOVA ERA
4895	NOVA LIMA
4897	NOVA MODICA
4899	NOVA PONTE
4901	NOVA RESENDE
4903	NOVA SERRANA
4905	NOVO CRUZEIRO
4907	OLARIA
4909	OLIMPIO NORONHA
4911	OLIVEIRA
4913	OLIVEIRA FORTES
4915	ONCA DE PITANGUI
4917	OURO BRANCO
4919	OURO FINO
4921	OURO PRETO
4923	OURO VERDE DE MINAS
4925	PADRE PARAISO
4927	PAINEIRAS
4929	PAINS
4931	PAIVA
4933	PALMA
4935	FRONTEIRA DOS VALES
4937	PAPAGAIOS
4939	PARACATU
4941	PARA DE MINAS
4943	PARAGUACU
4945	PARAISOPOLIS
4947	PARAOPEBA
4949	PASSABEM
4951	PASSA QUATRO
4953	PASSA TEMPO
4955	PASSA VINTE
4957	PASSOS
4959	PATOS DE MINAS
4961	PATROCINIO
4963	PATROCINIO DO MURIAE
4965	PAULA CANDIDO
4967	PAULISTAS
4969	PAVAO
4971	PECANHA
4973	PEDRA AZUL
4975	PEDRA DO ANTA
4977	PEDRA DO INDAIA
4979	PEDRA DOURADA
4981	PEDRALVA
4983	PEDRINOPOLIS
4985	PEDRO LEOPOLDO
4987	PEDRO TEIXEIRA
4989	PEQUERI
4991	PEQUI
4993	PERDIGAO
4995	PERDIZES
4997	PERDOES
4999	PESCADOR
5001	PIAU
5003	PIEDADE DE PONTE NOVA
5005	PIEDADE DO RIO GRANDE
5007	PIEDADE DOS GERAIS
5009	PIMENTA
5011	PIRACEMA
5013	PIRAJUBA
5015	PIRANGA
5017	PIRANGUCU
5019	PIRANGUINHO
5021	PIRAPETINGA
5023	PIRAPORA
5025	PIRAUBA
5027	PITANGUI
5029	PIUMHI
5031	PLANURA
5033	POCO FUNDO
5035	POCOS DE CALDAS
5037	POCRANE
5039	POMPEU
5041	PONTE NOVA
5043	PORTEIRINHA
5045	PORTO FIRME
5047	POTE
5049	POUSO ALEGRE
5051	POUSO ALTO
5053	PRADOS
5055	PRATA
5057	PRATAPOLIS
5059	PRATINHA
5061	PRESIDENTE BERNARDES
5063	PRESIDENTE JUSCELINO
5065	PRESIDENTE KUBITSCHEK
5067	PRESIDENTE OLEGARIO
5069	ALTO JEQUITIBA
5071	PRUDENTE DE MORAIS
5073	QUARTEL GERAL
5075	QUELUZITO
5077	RAPOSOS
5079	RAUL SOARES
5081	RECREIO
5083	RESENDE COSTA
5085	RESPLENDOR
5087	RESSAQUINHA
5089	RIACHO DOS MACHADOS
5091	RIBEIRAO DAS NEVES
5093	RIBEIRAO VERMELHO
5095	RIO ACIMA
5097	RIO CASCA
5099	RIO DOCE
5101	RIO DO PRADO
5103	RIO ESPERA
5105	RIO MANSO
5107	RIO NOVO
5109	RIO PARANAIBA
5111	RIO PARDO DE MINAS
5113	RIO PIRACICABA
5115	RIO POMBA
5117	RIO PRETO
5119	RIO VERMELHO
5121	RITAPOLIS
5123	ROCHEDO DE MINAS
5125	RODEIRO
5127	ROMARIA
5129	RUBELITA
5131	RUBIM
5133	SABARA
5135	SABINOPOLIS
5137	SACRAMENTO
5139	SALINAS
5141	SALTO DA DIVISA
5143	SANTA BARBARA
5145	SANTA BARBARA DO TUGURIO
5147	SANTA CRUZ DO ESCALVADO
5149	SANTA EFIGENIA DE MINAS
5151	SANTA FE DE MINAS
5153	SANTA JULIANA
5155	SANTA LUZIA
5157	SANTA MARGARIDA
5159	SANTA MARIA DE ITABIRA
5161	SANTA MARIA DO SALTO
5163	SANTA MARIA DO SUACUI
5165	SANTANA DA VARGEM
5167	SANTANA DE CATAGUASES
5169	SANTANA DE PIRAPAMA
5171	SANTANA DO DESERTO
5173	SANTANA DO GARAMBEU
5175	SANTANA DO JACARE
5177	SANTANA DO MANHUACU
5179	SANTANA DO RIACHO
5181	SANTANA DOS MONTES
5183	SANTA RITA DE CALDAS
5185	SANTA RITA DE JACUTINGA
5187	SANTA RITA DE IBITIPOCA
5189	SANTA RITA DO ITUETO
5191	SANTA RITA DO SAPUCAI
5193	SANTA ROSA DA SERRA
5195	SANTA VITORIA
5197	SANTO ANTONIO DO AMPARO
5199	SANTO ANTONIO DO AVENTUREIRO
5201	SANTO ANTONIO DO GRAMA
5203	SANTO ANTONIO DO ITAMBE
5205	SANTO ANTONIO DO JACINTO
5207	SANTO ANTONIO DO MONTE
5209	SANTO ANTONIO DO RIO ABAIXO
5211	SANTO HIPOLITO
5213	SANTOS DUMONT
5215	SAO BENTO ABADE
5217	SAO BRAS DO SUACUI
5219	SAO DOMINGOS DO PRATA
5221	SAO FRANCISCO
5223	SAO FRANCISCO DE PAULA
5225	SAO FRANCISCO DE SALES
5227	SAO FRANCISCO DO GLORIA
5229	SAO GERALDO
5231	SAO GERALDO DA PIEDADE
5233	SAO GONCALO DO ABAETE
5235	SAO GONCALO DO PARA
5237	SAO GONCALO DO RIO ABAIXO
5239	SAO GONCALO DO SAPUCAI
5241	SAO GOTARDO
5243	SAO JOAO BATISTA DO GLORIA
5245	SAO JOAO DA MATA
5247	SAO JOAO DA PONTE
5249	SAO JOAO DEL REI
5251	SAO JOAO DO ORIENTE
5253	SAO JOAO DO PARAISO
5255	SAO JOAO EVANGELISTA
5257	SAO JOAO NEPOMUCENO
5259	SAO JOSE DA SAFIRA
5261	SAO JOSE DA VARGINHA
5263	SAO JOSE DO ALEGRE
5265	SAO JOSE DO DIVINO
5267	SAO JOSE DO GOIABAL
5269	SAO JOSE DO JACURI
5271	SAO JOSE DO MANTIMENTO
5273	SAO LOURENCO
5275	SAO MIGUEL DO ANTA
5277	SAO PEDRO DA UNIAO
5279	SAO PEDRO DOS FERROS
5281	SAO PEDRO DO SUACUI
5283	SAO ROMAO
5285	SAO ROQUE DE MINAS
5287	SAO SEBASTIAO DA BELA VISTA
5289	SAO SEBASTIAO DO MARANHAO
5291	SAO SEBASTIAO DO OESTE
5293	SAO SEBASTIAO DO PARAISO
5295	SAO SEBASTIAO DO RIO PRETO
5297	SAO SEBASTIAO DO RIO VERDE
5299	SAO TIAGO
5301	SAO TOMAS DE AQUINO
5303	SAO TOME DAS LETRAS
5305	SAO VICENTE DE MINAS
5307	SAPUCAI-MIRIM
5309	SARDOA
5311	SENADOR CORTES
5313	SENADOR FIRMINO
5315	SENADOR JOSE BENTO
5317	SENADOR MODESTINO GONCALVES
5319	SENHORA DE OLIVEIRA
5321	SENHORA DO PORTO
5323	SENHORA DOS REMEDIOS
5325	SERICITA
5327	SERITINGA
5329	SERRA AZUL DE MINAS
5331	SERRA DA SAUDADE
5333	SERRA DOS AIMORES
5335	SERRA DO SALITRE
5337	SERRANIA
5339	SERRANOS
5341	SERRO
5343	SETE LAGOAS
5345	SILVEIRANIA
5347	SILVIANOPOLIS
5349	SIMAO PEREIRA
5351	SIMONESIA
5353	SOBRALIA
5355	SOLEDADE DE MINAS
5357	TABULEIRO
5359	TAIOBEIRAS
5361	TAPIRA
5363	TAPIRAI
5365	TAQUARACU DE MINAS
5367	TARUMIRIM
5369	TEIXEIRAS
5371	TEOFILO OTONI
5373	TIMOTEO
5375	TIRADENTES
5377	TIROS
5379	TOCANTINS
5381	TOLEDO
5383	TOMBOS
5385	TRES CORACOES
5387	TRES PONTAS
5389	TUMIRITINGA
5391	TUPACIGUARA
5393	TURMALINA
5395	TURVOLANDIA
5397	UBA
5399	UBAI
5401	UBERABA
5403	UBERLANDIA
5405	UMBURATIBA
5407	UNAI
5409	URUCANIA
5411	VARGEM BONITA
5413	VARGINHA
5415	VARZEA DA PALMA
5417	VARZELANDIA
5419	VAZANTE
5421	WENCESLAU BRAZ
5423	VERISSIMO
5425	VESPASIANO
5427	VICOSA
5429	VIEIRAS
5431	MATHIAS LOBATO
5433	VIRGEM DA LAPA
5435	VIRGINIA
5437	VIRGINOPOLIS
5439	VIRGOLANDIA
5441	VISCONDE DO RIO BRANCO
5443	VOLTA GRANDE
5445	SALTINHO
5447	SAO LOURENCO DA SERRA
5449	DOUTOR ULYSSES
5451	ITAPERUCU
5453	PINHAIS
5455	TUNAS DO PARANA
5457	NOVA SANTA BARBARA
5459	MAUA DA SERRA
5461	PITANGUEIRAS
5463	ANAHY
5465	DIAMANTE DO SUL
5467	IGUATU
5469	SANTA LUCIA
5471	BOA ESPERANCA DO IGUACU
5473	CRUZEIRO DO IGUACU
5475	FLOR DA SERRA DO SUL
5477	NOVA ESPERANCA DO SUDOESTE
5479	NOVA LARANJEIRAS
5481	RIO BONITO DO IGUACU
5483	VIRMOND
5485	IRACEMA DO OESTE
5487	MARIPA
5489	SAO PEDRO DO IGUACU
5491	CAFEZAL DO SUL
5493	SAUDADE DO IGUACU
5495	PINHAL DE SAO BENTO
5497	VENTANIA
5499	CANDOI
5501	LARANJAL
5503	MATO RICO
5505	SANTA MARIA DO OESTE
5507	LIDIANOPOLIS
5509	ANGULO
5511	FAROL
5513	RANCHO ALEGRE D'OESTE
5515	SAO MANOEL DO PARANA
5517	NOVO ITACOLOMI
5519	SANTA MONICA
5521	BRASILANDIA DO SUL
5523	ALTO PARAISO
5525	ITAIPULANDIA
5527	RAMILANDIA
5529	ENTRE RIOS DO OESTE
5531	MERCEDES
5533	PATO BRAGADO
5535	QUATRO PONTES
5537	BOMBINHAS
5539	MORRO GRANDE
5541	PASSO DE TORRES
5543	COCAL DO SUL
5545	CAPIVARI DE BAIXO
5547	SANGAO
5549	BALNEARIO BARRA DO SUL
5551	SAO JOAO DO ITAPERIU
5553	CALMON
5555	SANTA TEREZINHA
5557	BRACO DO TROMBUDO
5559	MIRIM DOCE
5561	MONTE CARLO
5563	VARGEM
5565	VARGEM BONITA
5567	CERRO NEGRO
5569	PONTE ALTA DO NORTE
5571	RIO RUFINO
5573	SAO CRISTOVAO DO SUL
5575	MACIEIRA
5577	AGUAS FRIAS
5579	CORDILHEIRA ALTA
5581	FORMOSA DO SUL
5583	GUATAMBU
5585	IRATI
5587	JARDINOPOLIS
5589	NOVA ITABERABA
5591	NOVO HORIZONTE
5593	PLANALTO ALEGRE
5595	SUL BRASIL
5597	ARABUTA
5599	ARVOREDO
5601	AFONSO CLAUDIO
5603	ALEGRE
5605	ALFREDO CHAVES
5607	ANCHIETA
5609	APIACA
5611	ARACRUZ
5613	ATILIO VIVACQUA
5615	BAIXO GUANDU
5617	BARRA DE SAO FRANCISCO
5619	BOA ESPERANCA
5621	BOM JESUS DO NORTE
5623	CACHOEIRO DE ITAPEMIRIM
5625	CARIACICA
5627	CASTELO
5629	COLATINA
5631	CONCEICAO DA BARRA
5633	CONCEICAO DO CASTELO
5635	DIVINO DE SAO LOURENCO
5637	DOMINGOS MARTINS
5639	DORES DO RIO PRETO
5641	ECOPORANGA
5643	FUNDAO
5645	GUACUI
5647	GUARAPARI
5649	IBIRACU
5651	ICONHA
5653	ITAGUACU
5655	ITAPEMIRIM
5657	ITARANA
5659	IUNA
5661	JERONIMO MONTEIRO
5663	LINHARES
5665	MANTENOPOLIS
5667	MIMOSO DO SUL
5669	MONTANHA
5671	MUCURICI
5673	MUNIZ FREIRE
5675	MUQUI
5677	NOVA VENECIA
5679	PANCAS
5681	PINHEIROS
5683	PIUMA
5685	PRESIDENTE KENNEDY
5687	RIO NOVO DO SUL
5689	SANTA LEOPOLDINA
5691	SANTA TERESA
5693	SAO GABRIEL DA PALHA
5695	SAO JOSE DO CALCADO
5697	SAO MATEUS
5699	SERRA
5701	VIANA
5703	VILA VELHA
5705	VITORIA
5707	MARILANDIA
5709	IBATIBA
5711	RIO BANANAL
5713	JAGUARE
5715	PEDRO CANARIO
5717	AGUA DOCE DO NORTE
5719	ALTO RIO NOVO
5721	JOAO NEIVA
5723	LARANJA DA TERRA
5725	SANTA MARIA DE JETIBA
5727	VARGEM ALTA
5729	VENDA NOVA DO IMIGRANTE
5731	ITAU DE MINAS
5733	AGUIA BRANCA
5735	CORONEL MARTINS
5737	IPUACU
5739	LAJEADO GRANDE
5741	OURO VERDE
5743	PASSOS MAIA
5745	BELMONTE
5747	PARAISO
5749	RIQUEZA
5751	SANTA HELENA
5753	SAO JOAO DO OESTE
5755	SAO MIGUEL DA BOA VISTA
5757	NOVA SANTA RITA
5759	MARIANA PIMENTEL
5761	SERTAO SANTANA
5763	GRAMADO XAVIER
5765	PASSO DO SOBRADO
5767	SINIMBU
5769	VALE DO SOL
5771	BARAO DO TRIUNFO
5773	MINAS DO LEAO
5775	MORRINHOS DO SUL
5777	TRES FORQUILHAS
5779	ARAMBARE
5781	SENTINELA DO SUL
5783	MAQUINE
5785	XANGRI-LA
5787	PINHAL GRANDE
5789	QUEVEDOS
5791	SAO JOAO DO POLESINE
5793	SAO MARTINHO DA SERRA
5795	VILA NOVA DO SUL
5797	COXILHA
5799	GENTIL
5801	ANGRA DOS REIS
5803	ARARUAMA
5805	BARRA DO PIRAI
5807	BARRA MANSA
5809	BOM JARDIM
5811	BOM JESUS DO ITABAPOANA
5813	CABO FRIO
5815	CACHOEIRAS DE MACACU
5817	CAMBUCI
5819	CAMPOS DOS GOYTACAZES
5821	CANTAGALO
5823	CARMO
5825	CASIMIRO DE ABREU
5827	CONCEICAO DE MACABU
5829	CORDEIRO
5831	DUAS BARRAS
5833	DUQUE DE CAXIAS
5835	ENGENHEIRO PAULO DE FRONTIN
5837	ITABORAI
5839	ITAGUAI
5841	ITAOCARA
5843	ITAPERUNA
5845	LAJE DO MURIAE
5847	MACAE
5849	MAGE
5851	MANGARATIBA
5853	MARICA
5855	MENDES
5857	MIGUEL PEREIRA
5859	MIRACEMA
5861	NATIVIDADE
5863	NILOPOLIS
5865	NITEROI
5867	NOVA FRIBURGO
5869	NOVA IGUACU
5871	PARACAMBI
5873	PARAIBA DO SUL
5875	PARATY
5877	PETROPOLIS
5879	PIRAI
5881	PORCIUNCULA
5883	RESENDE
5885	RIO BONITO
5887	RIO CLARO
5889	RIO DAS FLORES
5891	SANTA MARIA MADALENA
5893	SANTO ANTONIO DE PADUA
5895	SAO FIDELIS
5897	SAO GONCALO
5899	SAO JOAO DA BARRA
5901	SAO JOAO DE MERITI
5903	SAO PEDRO DA ALDEIA
5905	SAO SEBASTIAO DO ALTO
5907	SAPUCAIA
5909	SAQUAREMA
5911	SILVA JARDIM
5913	SUMIDOURO
5915	TERESOPOLIS
5917	TRAJANO DE MORAES
5919	TRES RIOS
5921	VALENCA
5923	VASSOURAS
5925	VOLTA REDONDA
5927	ARRAIAL DO CABO
5929	ITALVA
5931	MATO CASTELHANO
5933	MORMACO
5935	MULITERNO
5937	NICOLAU VERGUEIRO
5939	PONTAO
5941	SANTO ANTONIO DO PALMA
5943	BARRA FUNDA
5945	COQUEIROS DO SUL
5947	ENGENHO VELHO
5949	GRAMADO DOS LOUREIROS
5951	LAGOA DOS TRES CANTOS
5953	NOVA BOA VISTA
5955	RIO DOS INDIOS
5957	SANTO ANTONIO DO PLANALTO
5959	BARRA DO RIO AZUL
5961	CARLOS GOMES
5963	CENTENARIO
5965	CHARRUA
5967	PONTE PRETA
5969	AMETISTA DO SUL
5971	DOIS IRMAOS DAS MISSOES
5973	NOVO TIRADENTES
5975	PINHEIRINHO DO VALE
5977	SANTO EXPEDITO DO SUL
5979	TUPANCI DO SUL
5981	BOA VISTA DAS MISSOES
5983	LAJEADO DO BUGRE
5985	NOVO BARREIRO
5987	SAGRADA FAMILIA
5989	SAO JOSE DAS MISSOES
5991	NOVA PADUA
5993	MONTE BELO DO SUL
5995	SANTA TEREZA
5997	SAO VALENTIM DO SUL
5999	UNIAO DA SERRA
6001	RIO DE JANEIRO
6003	ITATIAIA
6005	PATY DO ALFERES
6007	QUISSAMA
6009	SAO JOSE DO VALE DO RIO PRETO
6011	IBITIRAMA
6013	CAMPESTRE DA SERRA
6015	SAO JOSE DOS AUSENTES
6017	LINDOLFO COLLOR
6019	MORRO REUTER
6021	PICADA CAFE
6023	PRESIDENTE LUCENA
6025	CAPITAO
6027	ITAPUCA
6029	COLINAS
6031	MATO LEITAO
6033	SANTA CLARA DO SUL
6035	SERIO
6037	TRAVESSEIRO
6039	MARATA
6041	PARECI NOVO
6043	SAO PEDRO DA SERRA
6045	ALTO FELIZ
6047	LINHA NOVA
6049	VALE REAL
6051	INHACORA
6053	VITORIA DAS MISSOES
6055	CORONEL BARROS
6057	NOVO MACHADO
6059	SAO JOSE DO INHACORA
6061	SALVADOR DAS MISSOES
6063	SAO PEDRO DO BUTIA
6065	PORTO MAUA
6067	PORTO VERA CRUZ
6069	BARRA DO GUARITA
6071	BOM PROGRESSO
6073	DERRUBADAS
6075	SAO VALERIO DO SUL
6077	TIRADENTES DO SUL
6079	MANOEL VIANA
6081	GARRUCHOS
6083	CANDIOTA
6085	HULHA NEGRA
6087	SAO JOSE DO POVO
6101	ADAMANTINA
6103	ADOLFO
6105	AGUAI
6107	AGUAS DA PRATA
6109	AGUAS DE LINDOIA
6111	AGUAS DE SAO PEDRO
6113	AGUDOS
6115	ALFREDO MARCONDES
6117	ALTAIR
6119	ALTINOPOLIS
6121	ALTO ALEGRE
6123	ALVARES FLORENCE
6125	ALVARES MACHADO
6127	ALVARO DE CARVALHO
6129	ALVINLANDIA
6131	AMERICANA
6133	AMERICO BRASILIENSE
6135	AMERICO DE CAMPOS
6137	AMPARO
6139	ANALANDIA
6141	ANDRADINA
6143	ANGATUBA
6145	ANHEMBI
6147	ANHUMAS
6149	APARECIDA
6151	APARECIDA D'OESTE
6153	APIAI
6155	ARACATUBA
6157	ARACOIABA DA SERRA
6159	ARAMINA
6161	ARANDU
6163	ARARAQUARA
6165	ARARAS
6167	AREALVA
6169	AREIAS
6171	AREIOPOLIS
6173	ARIRANHA
6175	ARTUR NOGUEIRA
6177	ARUJA
6179	ASSIS
6181	ATIBAIA
6183	AURIFLAMA
6185	AVAI
6187	AVANHANDAVA
6189	AVARE
6191	BADY BASSITT
6193	BALBINOS
6195	BALSAMO
6197	BANANAL
6199	BARBOSA
6201	BARAO DE ANTONINA
6203	BARIRI
6205	BARRA BONITA
6207	BARRA DO TURVO
6209	BARRETOS
6211	BARRINHA
6213	BARUERI
6215	BASTOS
6217	BATATAIS
6219	BAURU
6221	BEBEDOURO
6223	BENTO DE ABREU
6225	BERNARDINO DE CAMPOS
6227	BILAC
6229	BIRIGUI
6231	BIRITIBA-MIRIM
6233	BOA ESPERANCA DO SUL
6235	BOCAINA
6237	BOFETE
6239	BOITUVA
6241	BOM JESUS DOS PERDOES
6243	BORA
6245	BORACEIA
6247	BORBOREMA
6249	BOTUCATU
6251	BRAGANCA PAULISTA
6255	BRAUNA
6257	BRODOWSKI
6259	BROTAS
6261	BURI
6263	BURITAMA
6265	BURITIZAL
6267	CABRALIA PAULISTA
6269	CABREUVA
6271	CACAPAVA
6273	CACHOEIRA PAULISTA
6275	CACONDE
6277	CAFELANDIA
6279	CAIABU
6281	CAIEIRAS
6283	CAIUA
6285	CAJAMAR
6287	CAJOBI
6289	CAJURU
6291	CAMPINAS
6293	CAMPO LIMPO PAULISTA
6295	CAMPOS DO JORDAO
6297	CAMPOS NOVOS PAULISTA
6299	CANANEIA
6301	CANDIDO MOTA
6303	CANDIDO RODRIGUES
6305	CAPAO BONITO
6307	CAPELA DO ALTO
6309	CAPIVARI
6311	CARAGUATATUBA
6313	CARAPICUIBA
6315	CARDOSO
6317	CASA BRANCA
6319	CASSIA DOS COQUEIROS
6321	CASTILHO
6323	CATANDUVA
6325	CATIGUA
6327	CEDRAL
6329	CERQUEIRA CESAR
6331	CERQUILHO
6333	CESARIO LANGE
6335	CHARQUEADA
6337	CHAVANTES
6339	CLEMENTINA
6341	COLINA
6343	COLOMBIA
6345	CONCHAL
6347	CONCHAS
6349	CORDEIROPOLIS
6351	COROADOS
6353	CORONEL MACEDO
6355	CORUMBATAI
6357	COSMOPOLIS
6359	COSMORAMA
6361	COTIA
6363	CRAVINHOS
6365	CRISTAIS PAULISTA
6367	CRUZALIA
6369	CRUZEIRO
6371	CUBATAO
6373	CUNHA
6375	DESCALVADO
6377	DIADEMA
6379	DIVINOLANDIA
6381	DOBRADA
6383	DOIS CORREGOS
6385	DOLCINOPOLIS
6387	DOURADO
6389	DRACENA
6391	DUARTINA
6393	DUMONT
6395	ECHAPORA
6397	ELDORADO
6399	ELIAS FAUSTO
6401	EMBU DAS ARTES
6403	EMBU-GUACU
6405	ESTRELA D'OESTE
6407	ESTRELA DO NORTE
6409	FARTURA
6411	FERNANDOPOLIS
6413	FERNANDO PRESTES
6415	FERRAZ DE VASCONCELOS
6417	FLORA RICA
6419	FLOREAL
6421	FLORIDA PAULISTA
6423	FLORINEA
6425	FRANCA
6427	FRANCISCO MORATO
6429	FRANCO DA ROCHA
6431	GABRIEL MONTEIRO
6433	GALIA
6435	GARCA
6437	GASTAO VIDIGAL
6439	GENERAL SALGADO
6441	GETULINA
6443	GLICERIO
6445	GUAICARA
6447	GUAIMBE
6449	GUAIRA
6451	GUAPIACU
6453	GUAPIARA
6455	GUARA
6457	GUARACAI
6459	GUARACI
6461	GUARANI D'OESTE
6463	GUARANTA
6465	GUARARAPES
6467	GUARAREMA
6469	GUARATINGUETA
6471	GUAREI
6473	GUARIBA
6475	GUARUJA
6477	GUARULHOS
6479	GUZOLANDIA
6481	HERCULANDIA
6483	IACANGA
6485	IACRI
6487	IBATE
6489	IBIRA
6491	IBIRAREMA
6493	IBITINGA
6495	IBIUNA
6497	ICEM
6499	IEPE
6501	IGARACU DO TIETE
6503	IGARAPAVA
6505	IGARATA
6507	IGUAPE
6509	ILHABELA
6511	INDAIATUBA
6513	INDIANA
6515	INDIAPORA
6517	INUBIA PAULISTA
6519	IPAUSSU
6521	IPERO
6523	IPEUNA
6525	IPORANGA
6527	IPUA
6529	IRACEMAPOLIS
6531	IRAPUA
6533	IRAPURU
6535	ITABERA
6537	ITAI
6539	ITAJOBI
6541	ITAJU
6543	ITANHAEM
6545	ITAPECERICA DA SERRA
6547	ITAPETININGA
6549	ITAPEVA
6551	ITAPEVI
6553	ITAPIRA
6555	ITAPOLIS
6557	ITAPORANGA
6559	ITAPUI
6561	ITAPURA
6563	ITAQUAQUECETUBA
6565	ITARARE
6567	ITARIRI
6569	ITATIBA
6571	ITATINGA
6573	ITIRAPINA
6575	ITIRAPUA
6577	ITOBI
6579	ITU
6581	ITUPEVA
6583	ITUVERAVA
6585	JABORANDI
6587	JABOTICABAL
6589	JACAREI
6591	JACI
6593	JACUPIRANGA
6595	JAGUARIUNA
6597	JALES
6599	JAMBEIRO
6601	JANDIRA
6603	JARDINOPOLIS
6605	JARINU
6607	JAU
6609	JERIQUARA
6611	JOANOPOLIS
6613	JOAO RAMALHO
6615	JOSE BONIFACIO
6617	JULIO MESQUITA
6619	JUNDIAI
6621	JUNQUEIROPOLIS
6623	JUQUIA
6625	JUQUITIBA
6627	LAGOINHA
6629	LARANJAL PAULISTA
6631	LAVINIA
6633	LAVRINHAS
6635	LEME
6637	LENCOIS PAULISTA
6639	LIMEIRA
6641	LINDOIA
6643	LINS
6645	LORENA
6647	LOUVEIRA
6649	LUCELIA
6651	LUCIANOPOLIS
6653	LUIS ANTONIO
6655	LUIZIANIA
6657	LUPERCIO
6659	LUTECIA
6661	MACATUBA
6663	MACAUBAL
6665	MACEDONIA
6667	MAGDA
6669	MAIRINQUE
6671	MAIRIPORA
6673	MANDURI
6675	MARABA PAULISTA
6677	MARACAI
6679	MARIAPOLIS
6681	MARILIA
6683	MARINOPOLIS
6685	MARTINOPOLIS
6687	MATAO
6689	MAUA
6691	MENDONCA
6693	MERIDIANO
6695	MIGUELOPOLIS
6697	MINEIROS DO TIETE
6699	MIRACATU
6701	MIRA ESTRELA
6703	MIRANDOPOLIS
6705	MIRANTE DO PARANAPANEMA
6707	MIRASSOL
6709	MIRASSOLANDIA
6711	MOCOCA
6713	MOGI DAS CRUZES
6715	MOGI-GUACU
6717	MOGI MIRIM
6719	MOMBUCA
6721	MONCOES
6723	MONGAGUA
6725	MONTE ALEGRE DO SUL
6727	MONTE ALTO
6729	MONTE APRAZIVEL
6731	MONTE AZUL PAULISTA
6733	MONTE CASTELO
6735	MONTEIRO LOBATO
6737	MONTE MOR
6739	MORRO AGUDO
6741	MORUNGABA
6743	MURUTINGA DO SUL
6745	NARANDIBA
6747	NATIVIDADE DA SERRA
6749	NAZARE PAULISTA
6751	NEVES PAULISTA
6753	NHANDEARA
6755	NIPOA
6757	NOVA ALIANCA
6759	NOVA EUROPA
6761	NOVA GRANADA
6763	NOVA GUATAPORANGA
6765	NOVA INDEPENDENCIA
6767	NOVA LUZITANIA
6769	NOVA ODESSA
6771	NOVO HORIZONTE
6773	NUPORANGA
6775	OCAUCU
6777	OLEO
6779	OLIMPIA
6781	ONDA VERDE
6783	ORIENTE
6785	ORINDIUVA
6787	ORLANDIA
6789	OSASCO
6791	OSCAR BRESSANE
6793	OSVALDO CRUZ
6795	OURINHOS
6797	OURO VERDE
6799	PACAEMBU
6801	PALESTINA
6803	PALMARES PAULISTA
6805	PALMEIRA D'OESTE
6807	PALMITAL
6809	PANORAMA
6811	PARAGUACU PAULISTA
6813	PARAIBUNA
6815	PARAISO
6817	PARANAPANEMA
6819	PARANAPUA
6821	PARAPUA
6823	PARDINHO
6825	PARIQUERA-ACU
6827	PATROCINIO PAULISTA
6829	PAULICEIA
6831	PAULINIA
6833	PAULO DE FARIA
6835	PEDERNEIRAS
6837	PEDRA BELA
6839	PEDRANOPOLIS
6841	PEDREGULHO
6843	PEDREIRA
6845	PEDRO DE TOLEDO
6847	PENAPOLIS
6849	PEREIRA BARRETO
6851	PEREIRAS
6853	PERUIBE
6855	PIACATU
6857	PIEDADE
6859	PILAR DO SUL
6861	PINDAMONHANGABA
6863	PINDORAMA
6865	ESPIRITO SANTO DO PINHAL
6867	PINHALZINHO
6869	PIQUEROBI
6871	PIQUETE
6873	PIRACAIA
6875	PIRACICABA
6877	PIRAJU
6879	PIRAJUI
6881	PIRANGI
6883	PIRAPORA DO BOM JESUS
6885	PIRAPOZINHO
6887	PIRASSUNUNGA
6889	PIRATININGA
6891	PITANGUEIRAS
6893	PLANALTO
6895	PLATINA
6897	POA
6899	POLONI
6901	POMPEIA
6903	PONGAI
6905	PONTAL
6907	PONTES GESTAL
6909	POPULINA
6911	PORANGABA
6913	PORTO FELIZ
6915	PORTO FERREIRA
6917	POTIRENDABA
6919	PRADOPOLIS
6921	PRAIA GRANDE
6923	PRESIDENTE ALVES
6925	PRESIDENTE BERNARDES
6927	PRESIDENTE EPITACIO
6929	PRESIDENTE PRUDENTE
6931	PRESIDENTE VENCESLAU
6933	PROMISSAO
6935	QUATA
6937	QUEIROZ
6939	QUELUZ
6941	QUINTANA
6943	RAFARD
6945	RANCHARIA
6947	REDENCAO DA SERRA
6949	REGENTE FEIJO
6951	REGINOPOLIS
6953	REGISTRO
6955	RESTINGA
6957	RIBEIRA
6959	RIBEIRAO BONITO
6961	RIBEIRAO BRANCO
6963	RIBEIRAO CORRENTE
6965	RIBEIRAO DO SUL
6967	RIBEIRAO PIRES
6969	RIBEIRAO PRETO
6971	RIVERSUL
6973	RIFAINA
6975	RINCAO
6977	RINOPOLIS
6979	RIO CLARO
6981	RIO DAS PEDRAS
6983	RIO GRANDE DA SERRA
6985	RIOLANDIA
6987	ROSEIRA
6989	RUBIACEA
6991	RUBINEIA
6993	SABINO
6995	SAGRES
6997	SALES
6999	SALES OLIVEIRA
7001	SALESOPOLIS
7003	SALMOURAO
7005	SALTO
7007	SALTO DE PIRAPORA
7009	SALTO GRANDE
7011	SANDOVALINA
7013	SANTA ADELIA
7015	SANTA ALBERTINA
7017	SANTA BARBARA D'OESTE
7019	AGUAS DE SANTA BARBARA
7021	SANTA BRANCA
7023	SANTA CLARA D'OESTE
7025	SANTA CRUZ DA CONCEICAO
7027	SANTA CRUZ DAS PALMEIRAS
7029	SANTA CRUZ DO RIO PARDO
7031	SANTA ERNESTINA
7033	SANTA FE DO SUL
7035	SANTA GERTRUDES
7037	SANTA ISABEL
7039	SANTA LUCIA
7041	SANTA MARIA DA SERRA
7043	SANTA MERCEDES
7045	SANTANA DA PONTE PENSA
7047	SANTANA DE PARNAIBA
7049	SANTA RITA D'OESTE
7051	SANTA RITA DO PASSA QUATRO
7053	SANTA ROSA DE VITERBO
7055	SANTO ANASTACIO
7057	SANTO ANDRE
7059	SANTO ANTONIO DA ALEGRIA
7061	SANTO ANTONIO DE POSSE
7063	SANTO ANTONIO DO JARDIM
7065	SANTO ANTONIO DO PINHAL
7067	SANTO EXPEDITO
7069	SANTOPOLIS DO AGUAPEI
7071	SANTOS
7073	SAO BENTO DO SAPUCAI
7075	SAO BERNARDO DO CAMPO
7077	SAO CAETANO DO SUL
7079	SAO CARLOS
7081	SAO FRANCISCO
7083	SAO JOAO DA BOA VISTA
7085	SAO JOAO DAS DUAS PONTES
7087	SAO JOAO DO PAU D'ALHO
7089	SAO JOAQUIM DA BARRA
7091	SAO JOSE DA BELA VISTA
7093	SAO JOSE DO BARREIRO
7095	SAO JOSE DO RIO PARDO
7097	SAO JOSE DO RIO PRETO
7099	SAO JOSE DOS CAMPOS
7101	SAO LUIZ DO PARAITINGA
7103	SAO MANUEL
7105	SAO MIGUEL ARCANJO
7107	SAO PAULO
7109	SAO PEDRO
7111	SAO PEDRO DO TURVO
7113	SAO ROQUE
7115	SAO SEBASTIAO
7117	SAO SEBASTIAO DA GRAMA
7119	SAO SIMAO
7121	SAO VICENTE
7123	SARAPUI
7125	SARUTAIA
7127	SEBASTIANOPOLIS DO SUL
7129	SERRA AZUL
7131	SERRANA
7133	SERRA NEGRA
7135	SERTAOZINHO
7137	SETE BARRAS
7139	SEVERINIA
7141	SILVEIRAS
7143	SOCORRO
7145	SOROCABA
7147	SUD MENNUCCI
7149	SUMARE
7151	SUZANO
7153	TABAPUA
7155	TABATINGA
7157	TABOAO DA SERRA
7159	TACIBA
7161	TAGUAI
7163	TAIACU
7165	TAIUVA
7167	TAMBAU
7169	TANABI
7171	TAPIRAI
7173	TAPIRATIBA
7175	TAQUARITINGA
7177	TAQUARITUBA
7179	TARABAI
7181	TATUI
7183	TAUBATE
7185	TEJUPA
7187	TEODORO SAMPAIO
7189	TERRA ROXA
7191	TIETE
7193	TIMBURI
7195	TORRINHA
7197	TREMEMBE
7199	TRES FRONTEIRAS
7201	TUPA
7203	TUPI PAULISTA
7205	TURIUBA
7207	TURMALINA
7209	UBATUBA
7211	UBIRAJARA
7213	UCHOA
7215	UNIAO PAULISTA
7217	URANIA
7219	URU
7221	URUPES
7223	VALENTIM GENTIL
7225	VALINHOS
7227	VALPARAISO
7231	VARGEM GRANDE DO SUL
7233	VARZEA PAULISTA
7235	VERA CRUZ
7237	VINHEDO
7239	VIRADOURO
7241	VISTA ALEGRE DO ALTO
7243	VOTORANTIM
7245	VOTUPORANGA
7247	BOREBI
7249	DIRCE REIS
7251	EMBAUBA
7253	ESPIRITO SANTO DO TURVO
7255	EUCLIDES DA CUNHA PAULISTA
7257	GUATAPARA
7259	IARAS
7263	MOTUCA
7265	ROSANA
7267	TARUMA
7273	VARGEM GRANDE PAULISTA
7293	SAO VENDELINO
7295	IMIGRANTE
7297	IMBE
7299	IBIRAPUITA
7301	ESTACAO
7303	VISTA GAUCHA
7305	VISTA ALEGRE DO PRATA
7307	VISTA ALEGRE
7309	VILA MARIA
7311	VILA FLORES
7313	TAQUARUCU DO SUL
7315	SILVEIRA MARTINS
7317	SEGREDO
7319	VANINI
7321	TUPANDI
7323	TUNAS
7325	TRINDADE DO SUL
7327	TRES PALMEIRAS
7329	TRES CACHOEIRAS
7331	TRES ARROIOS
7333	TERRA DE AREIA
7335	SEDE NOVA
7337	SANTA MARIA DO HERVAL
7339	SALDANHA MARINHO
7341	SAO MIGUEL DAS MISSOES
7343	SAO JOSE DO HORTENCIO
7345	SAO JOSE DO HERVAL
7347	SAO JORGE
7349	SAO JOAO DA URTIGA
7351	SAO DOMINGOS DO SUL
7353	RIOZINHO
7355	RELVADO
7357	QUINZE DE NOVEMBRO
7359	PROTASIO ALVES
7361	PROGRESSO
7363	POUSO NOVO
7365	POCO DAS ANTAS
7367	PIRAPO
7369	PINHAL
7371	PAVERAMA
7373	PARAISO DO SUL
7375	PANTANO GRANDE
7377	NOVA ROMA DO SUL
7379	NOVA HARTZ
7381	NOVA ESPERANCA DO SUL
7383	NOVA ALVORADA
7385	MORRO REDONDO
7387	MONTAURI
7389	LAGOAO
7391	JAQUIRANA
7393	JABOTICABA
7395	IVORA
7397	ITACURUBI
7399	IPIRANGA DO SUL
7401	ABATIA
7403	ADRIANOPOLIS
7405	AGUDOS DO SUL
7407	ALMIRANTE TAMANDARE
7409	ALTO PARANA
7411	ALTO PIQUIRI
7413	ALVORADA DO SUL
7415	AMAPORA
7417	AMPERE
7419	ANDIRA
7421	ANTONINA
7423	ANTONIO OLINTO
7425	APUCARANA
7427	ARAPONGAS
7429	ARAPOTI
7431	ARARUNA
7433	MARILANDIA DO SUL
7435	ARAUCARIA
7437	ASSAI
7439	ASTORGA
7441	ATALAIA
7443	BALSA NOVA
7445	BANDEIRANTES
7447	BARBOSA FERRAZ
7449	BARRACAO
7451	BARRA DO JACARE
7453	BELA VISTA DO PARAISO
7455	BITURUNA
7457	BOA ESPERANCA
7459	BOCAIUVA DO SUL
7461	BOM SUCESSO
7463	BORRAZOPOLIS
7465	CAFEARA
7467	CALIFORNIA
7469	CAMBARA
7471	CAMBE
7473	CAMBIRA
7475	CAMPINA DA LAGOA
7477	CAMPINA GRANDE DO SUL
7479	CAMPO DO TENENTE
7481	CAMPO LARGO
7483	CAMPO MOURAO
7485	CANDIDO DE ABREU
7487	CAPANEMA
7489	CAPITAO LEONIDAS MARQUES
7491	CARLOPOLIS
7493	CASCAVEL
7495	CASTRO
7497	CATANDUVAS
7499	CENTENARIO DO SUL
7501	CERRO AZUL
7503	CHOPINZINHO
7505	CIANORTE
7507	CIDADE GAUCHA
7509	CLEVELANDIA
7511	MANGUEIRINHA
7513	COLOMBO
7515	COLORADO
7517	CONGONHINHAS
7519	CONSELHEIRO MAIRINCK
7521	CONTENDA
7523	CORBELIA
7525	CORNELIO PROCOPIO
7527	CORONEL VIVIDA
7529	CRUZEIRO DO OESTE
7531	CRUZEIRO DO SUL
7533	CRUZ MACHADO
7535	CURITIBA
7537	CURIUVA
7539	DIAMANTE DO NORTE
7541	DOIS VIZINHOS
7543	DOUTOR CAMARGO
7545	ENEAS MARQUES
7547	ENGENHEIRO BELTRAO
7549	FAXINAL
7551	FENIX
7553	FLORAI
7555	FLORESTA
7557	FLORESTOPOLIS
7559	FLORIDA
7561	FORMOSA DO OESTE
7563	FOZ DO IGUACU
7565	FRANCISCO BELTRAO
7567	GENERAL CARNEIRO
7569	GOIOERE
7571	GUAIRA
7573	GUAIRACA
7575	GUAPIRAMA
7577	GUAPOREMA
7579	GUARACI
7581	GUARANIACU
7583	GUARAPUAVA
7585	GUARAQUECABA
7587	GUARATUBA
7589	IBAITI
7591	IBIPORA
7593	ICARAIMA
7595	IGUARACU
7597	IMBITUVA
7599	INACIO MARTINS
7601	INAJA
7603	IPIRANGA
7605	IPORA
7607	IRATI
7609	IRETAMA
7611	ITAGUAJE
7613	ITAMBARACA
7615	ITAMBE
7617	ITAPEJARA D'OESTE
7619	ITAUNA DO SUL
7621	IVAI
7623	IVAIPORA
7625	IVATUBA
7627	JABOTI
7629	JACAREZINHO
7631	JAGUAPITA
7633	JAGUARIAIVA
7635	JANDAIA DO SUL
7637	JANIOPOLIS
7639	JAPIRA
7641	JAPURA
7643	JARDIM ALEGRE
7645	JARDIM OLINDA
7647	JATAIZINHO
7649	JOAQUIM TAVORA
7651	JUNDIAI DO SUL
7653	JUSSARA
7655	KALORE
7657	LAPA
7659	LARANJEIRAS DO SUL
7661	LEOPOLIS
7663	LOANDA
7665	LOBATO
7667	LONDRINA
7669	LUPIONOPOLIS
7671	MALLET
7673	MAMBORE
7675	MANDAGUACU
7677	MANDAGUARI
7679	MANDIRITUBA
7681	MANOEL RIBAS
7683	MARECHAL CANDIDO RONDON
7685	MARIA HELENA
7687	MARIALVA
7689	MARILUZ
7691	MARINGA
7693	MARIOPOLIS
7695	MARMELEIRO
7697	MARUMBI
7699	MATELANDIA
7701	MEDIANEIRA
7703	MIRADOR
7705	MIRASELVA
7707	MOREIRA SALES
7709	MORRETES
7711	MUNHOZ DE MELO
7713	NOSSA SENHORA DAS GRACAS
7715	NOVA ALIANCA DO IVAI
7717	NOVA AMERICA DA COLINA
7719	NOVA CANTU
7721	NOVA ESPERANCA
7723	NOVA FATIMA
7725	NOVA LONDRINA
7727	ORTIGUEIRA
7729	OURIZONA
7731	PAICANDU
7733	PALMAS
7735	PALMEIRA
7737	PALMITAL
7739	PALOTINA
7741	PARAISO DO NORTE
7743	PARANACITY
7745	PARANAGUA
7747	PARANAPOEMA
7749	PARANAVAI
7751	PATO BRANCO
7753	PAULA FREITAS
7755	PAULO FRONTIN
7757	PEABIRU
7759	PEROLA D'OESTE
7761	PIEN
7763	PINHALAO
7765	PINHAO
7767	PIRAI DO SUL
7769	PIRAQUARA
7771	PITANGA
7773	PLANALTINA DO PARANA
7775	PLANALTO
7777	PONTA GROSSA
7779	PORECATU
7781	PORTO AMAZONAS
7783	PORTO RICO
7785	PORTO VITORIA
7787	PRESIDENTE CASTELO BRANCO
7789	PRIMEIRO DE MAIO
7791	PRUDENTOPOLIS
7793	QUATIGUA
7795	QUATRO BARRAS
7797	QUERENCIA DO NORTE
7799	QUINTA DO SOL
7801	QUITANDINHA
7803	RANCHO ALEGRE
7805	REALEZA
7807	REBOUCAS
7809	RENASCENCA
7811	RESERVA
7813	RIBEIRAO CLARO
7815	RIBEIRAO DO PINHAL
7817	RIO AZUL
7819	RIO BOM
7821	RIO BRANCO DO SUL
7823	RIO NEGRO
7825	ROLANDIA
7827	RONCADOR
7829	RONDON
7831	SABAUDIA
7833	SALGADO FILHO
7835	SALTO DO ITARARE
7837	SALTO DO LONTRA
7839	SANTA AMELIA
7841	SANTA CECILIA DO PAVAO
7843	SANTA CRUZ DE MONTE CASTELO
7845	SANTA FE
7847	SANTA INES
7849	SANTA ISABEL DO IVAI
7851	SANTA IZABEL DO OESTE
7853	SANTA MARIANA
7855	SANTANA DO ITARARE
7857	SANTO ANTONIO DO SUDOESTE
7859	SANTO ANTONIO DA PLATINA
7861	SANTO ANTONIO DO CAIUA
7863	SANTO ANTONIO DO PARAISO
7865	SANTO INACIO
7867	SAO CARLOS DO IVAI
7869	SAO JERONIMO DA SERRA
7871	SAO JOAO
7873	SAO JOAO DO CAIUA
7875	SAO JOAO DO IVAI
7877	SAO JOAO DO TRIUNFO
7879	SAO JORGE DO IVAI
7881	SAO JORGE D'OESTE
7883	SAO JOSE DA BOA VISTA
7885	SAO JOSE DOS PINHAIS
7887	SAO MATEUS DO SUL
7889	SAO MIGUEL DO IGUACU
7891	SAO PEDRO DO IVAI
7893	SAO PEDRO DO PARANA
7895	SAO SEBASTIAO DA AMOREIRA
7897	SAO TOME
7899	SAPOPEMA
7901	SENGES
7903	SERTANEJA
7905	SERTANOPOLIS
7907	SIQUEIRA CAMPOS
7909	TAMBOARA
7911	TAPEJARA
7913	TEIXEIRA SOARES
7915	TELEMACO BORBA
7917	TERRA BOA
7919	TERRA RICA
7921	TERRA ROXA
7923	TIBAGI
7925	TIJUCAS DO SUL
7927	TOLEDO
7929	TOMAZINA
7931	TUNEIRAS DO OESTE
7933	UBIRATA
7935	UMUARAMA
7937	UNIAO DA VITORIA
7939	UNIFLOR
7941	URAI
7943	WENCESLAU BRAZ
7945	VERE
7947	VITORINO
7949	XAMBRE
7951	ALTONIA
7953	ASSIS CHATEAUBRIAND
7955	QUEDAS DO IGUACU
7957	CEU AZUL
7959	GRANDES RIOS
7961	INDIANOPOLIS
7963	MATINHOS
7965	NOVA AURORA
7967	NOVA OLIMPIA
7969	PEROLA
7971	SANTA HELENA
7973	TAPIRA
7975	MARILENA
7977	FRANCISCO ALVES
7979	NOVA SANTA ROSA
7981	BOA VISTA DA APARECIDA
7983	BRAGANEY
7985	CAFELANDIA
7987	TRES BARRAS DO PARANA
7989	VERA CRUZ DO OESTE
7991	PRANCHITA
7993	TUPASSI
7995	NOVA PRATA DO IGUACU
7997	JESUITAS
7999	SAO JORGE DO PATROCINIO
8001	ABELARDO LUZ
8003	AGROLANDIA
8005	AGRONOMICA
8007	AGUA DOCE
8009	AGUAS DE CHAPECO
8011	AGUAS MORNAS
8013	ALFREDO WAGNER
8015	ANCHIETA
8017	ANGELINA
8019	ANITA GARIBALDI
8021	ANITAPOLIS
8023	ANTONIO CARLOS
8025	ARAQUARI
8027	ARARANGUA
8029	ARMAZEM
8031	ARROIO TRINTA
8033	ASCURRA
8035	ATALANTA
8037	AURORA
8039	BALNEARIO CAMBORIU
8041	BARRA VELHA
8043	BENEDITO NOVO
8045	BIGUACU
8047	BLUMENAU
8049	BOM RETIRO
8051	BOTUVERA
8053	BRACO DO NORTE
8055	BRUSQUE
8057	CACADOR
8059	CAIBI
8061	CAMBORIU
8063	CAMPO ALEGRE
8065	CAMPO BELO DO SUL
8067	CAMPO ERE
8069	CAMPOS NOVOS
8071	CANELINHA
8073	CANOINHAS
8075	CAPINZAL
8077	CATANDUVAS
8079	CAXAMBU DO SUL
8081	CHAPECO
8083	CONCORDIA
8085	CORONEL FREITAS
8087	CORUPA
8089	CRICIUMA
8091	CUNHA PORA
8093	CURITIBANOS
8095	DESCANSO
8097	DIONISIO CERQUEIRA
8099	DONA EMMA
8101	ERVAL VELHO
8103	FAXINAL DOS GUEDES
8105	FLORIANOPOLIS
8107	FRAIBURGO
8109	GALVAO
8111	GOVERNADOR CELSO RAMOS
8113	GAROPABA
8115	GARUVA
8117	GASPAR
8119	GRAO PARA
8121	GRAVATAL
8123	GUABIRUBA
8125	GUARACIABA
8127	GUARAMIRIM
8129	GUARUJA DO SUL
8131	HERVAL D'OESTE
8133	IBICARE
8135	IBIRAMA
8137	ICARA
8139	ILHOTA
8141	IMARUI
8143	IMBITUBA
8145	IMBUIA
8147	INDAIAL
8149	IPIRA
8151	IPUMIRIM
8153	IRANI
8155	IRINEOPOLIS
8157	ITA
8159	ITAIOPOLIS
8161	ITAJAI
8163	ITAPEMA
8165	ITAPIRANGA
8167	ITUPORANGA
8169	JABORA
8171	JACINTO MACHADO
8173	JAGUARUNA
8175	JARAGUA DO SUL
8177	JOACABA
8179	JOINVILLE
8181	LACERDOPOLIS
8183	LAGES
8185	LAGUNA
8187	LAURENTINO
8189	LAURO MULLER
8191	LEBON REGIS
8193	LEOBERTO LEAL
8195	LONTRAS
8197	LUIZ ALVES
8199	MAFRA
8201	MAJOR GERCINO
8203	MAJOR VIEIRA
8205	MARAVILHA
8207	MASSARANDUBA
8209	MATOS COSTA
8211	MELEIRO
8213	MODELO
8215	MONDAI
8217	MONTE CASTELO
8219	MORRO DA FUMACA
8221	NAVEGANTES
8223	NOVA ERECHIM
8225	NOVA TRENTO
8227	NOVA VENEZA
8229	ORLEANS
8231	OURO
8233	PALHOCA
8235	PALMA SOLA
8237	PALMITOS
8239	PAPANDUVA
8241	PAULO LOPES
8243	PEDRAS GRANDES
8245	PENHA
8247	PERITIBA
8249	PETROLANDIA
8251	BALNEARIO DE PICARRAS
8253	PINHALZINHO
8255	PINHEIRO PRETO
8257	PIRATUBA
8259	POMERODE
8261	PONTE ALTA
8263	PONTE SERRADA
8265	PORTO BELO
8267	PORTO UNIAO
8269	POUSO REDONDO
8271	PRAIA GRANDE
8273	PRESIDENTE CASTELLO BRANCO
8275	PRESIDENTE GETULIO
8277	PRESIDENTE NEREU
8279	QUILOMBO
8281	RANCHO QUEIMADO
8283	RIO DAS ANTAS
8285	RIO DO CAMPO
8287	RIO DO OESTE
8289	RIO DOS CEDROS
8291	RIO DO SUL
8293	RIO FORTUNA
8295	RIO NEGRINHO
8297	RODEIO
8299	ROMELANDIA
8301	SALETE
8303	SALTO VELOSO
8305	SANTA CECILIA
8307	SANTA ROSA DE LIMA
8309	SANTO AMARO DA IMPERATRIZ
8311	SAO BENTO DO SUL
8313	SAO BONIFACIO
8315	SAO CARLOS
8317	SAO DOMINGOS
8319	SAO FRANCISCO DO SUL
8321	SAO JOAO BATISTA
8323	SAO JOAO DO SUL
8325	SAO JOAQUIM
8327	SAO JOSE
8329	SAO JOSE DO CEDRO
8331	SAO JOSE DO CERRITO
8333	SAO LOURENCO DO OESTE
8335	SAO LUDGERO
8337	SAO MARTINHO
8339	SAO MIGUEL DO OESTE
8341	SAUDADES
8343	SCHROEDER
8345	SEARA
8347	SIDEROPOLIS
8349	SOMBRIO
8351	TAIO
8353	TANGARA
8355	TIJUCAS
8357	TIMBO
8359	TRES BARRAS
8361	TREZE DE MAIO
8363	TREZE TILIAS
8365	TROMBUDO CENTRAL
8367	TUBARAO
8369	TURVO
8371	URUBICI
8373	URUSSANGA
8375	VARGEAO
8377	VIDAL RAMOS
8379	VIDEIRA
8381	WITMARSUM
8383	XANXERE
8385	XAVANTINA
8387	XAXIM
8389	BOM JARDIM DA SERRA
8391	MARACAJA
8393	TIMBE DO SUL
8395	CORREIA PINTO
8397	OTACILIO COSTA
8399	IPE
8401	IBARAMA
8403	HARMONIA
8405	GUABIJU
8407	GLORINHA
8409	FAXINALZINHO
8411	FAGUNDES VARELA
8413	EUGENIO DE CASTRO
8415	ERNESTINA
8417	EREBANGO
8419	ENTRE IJUIS
8421	ENTRE RIOS DO SUL
8423	ELDORADO DO SUL
8425	DOUTOR MAURICIO CARDOSO
8427	DOIS LAJEADOS
8429	DEZESSEIS DE NOVEMBRO
8431	CRISTAL
8433	CIDREIRA
8435	CERRO GRANDE DO SUL
8437	CERRO GRANDE
8439	CERRO BRANCO
8441	CASEIROS
8443	CAPELA DE SANTANA
8445	CAMPOS BORGES
8447	CAMARGO
8449	BROCHIER
8451	CANTAGALO
8453	TURVO
8455	ALTAMIRA DO PARANA
8457	FIGUEIRA
8459	LUNARDELLI
8461	SARANDI
8463	JURANDA
8465	DOURADINA
8467	SANTA TEREZINHA DE ITAIPU
8469	MISSAL
8471	SAO JOSE DAS PALMEIRAS
8473	ROSARIO DO IVAI
8475	CAMPO BONITO
8477	SULINA
8479	CORUMBATAI DO SUL
8481	LUIZIANA
8483	BOQUEIRAO DO LEAO
8485	BARAO
8487	AUREA
8489	ARROIO DO SAL
8491	ANDRE DA ROCHA
8493	AMARAL FERRADOR
8495	ALTO ALEGRE
8497	ALEGRIA
8499	AGUA SANTA
8501	AGUDO
8503	AJURICABA
8505	ALECRIM
8507	ALEGRETE
8509	ALPESTRE
8511	ALVORADA
8513	ANTA GORDA
8515	ANTONIO PRADO
8517	ARATIBA
8519	ARROIO DO MEIO
8521	ARROIO DOS RATOS
8523	ARROIO DO TIGRE
8525	ARROIO GRANDE
8527	ARVOREZINHA
8529	AUGUSTO PESTANA
8531	BAGE
8533	BARAO DE COTEGIPE
8535	BARRACAO
8537	BARRA DO RIBEIRO
8539	BARROS CASSAL
8541	BENTO GONCALVES
8543	BOA VISTA DO BURICA
8545	BOM JESUS
8547	BOM RETIRO DO SUL
8549	BOSSOROCA
8551	BRAGA
8553	BUTIA
8555	CACAPAVA DO SUL
8557	CACEQUI
8559	CACHOEIRA DO SUL
8561	CACHOEIRINHA
8563	CACIQUE DOBLE
8565	CAIBATE
8567	CAICARA
8569	CAMAQUA
8571	CAMBARA DO SUL
8573	CAMPINA DAS MISSOES
8575	CAMPINAS DO SUL
8577	CAMPO BOM
8579	CAMPO NOVO
8581	CANDELARIA
8583	CANDIDO GODOI
8585	CANELA
8587	CANGUCU
8589	CANOAS
8591	CARAZINHO
8593	CARLOS BARBOSA
8595	CASCA
8597	CATUIPE
8599	CAXIAS DO SUL
8601	CERRO LARGO
8603	CHAPADA
8605	CHIAPETTA
8607	CIRIACO
8609	COLORADO
8611	CONDOR
8613	CONSTANTINA
8615	CORONEL BICACO
8617	CRISSIUMAL
8619	CRUZ ALTA
8621	CRUZEIRO DO SUL
8623	DAVID CANABARRO
8625	DOIS IRMAOS
8627	DOM FELICIANO
8629	DOM PEDRITO
8631	DONA FRANCISCA
8633	ENCANTADO
8635	ENCRUZILHADA DO SUL
8637	ERECHIM
8639	HERVAL
8641	ERVAL GRANDE
8643	ERVAL SECO
8645	ESMERALDA
8647	ESPUMOSO
8649	ESTANCIA VELHA
8651	ESTEIO
8653	ESTRELA
8655	FARROUPILHA
8657	FAXINAL DO SOTURNO
8659	FELIZ
8661	FLORES DA CUNHA
8663	FONTOURA XAVIER
8665	FORMIGUEIRO
8667	FREDERICO WESTPHALEN
8669	GARIBALDI
8671	GAURAMA
8673	GENERAL CAMARA
8675	SAO VICENTE DO SUL
8677	GETULIO VARGAS
8679	GIRUA
8681	GRAMADO
8683	GRAVATAI
8685	GUAIBA
8687	GUAPORE
8689	GUARANI DAS MISSOES
8691	HORIZONTINA
8693	CHARQUEADAS
8695	HUMAITA
8697	IBIACA
8699	IBIRAIARAS
8701	IBIRUBA
8703	IGREJINHA
8705	IJUI
8707	ILOPOLIS
8709	INDEPENDENCIA
8711	IRAI
8713	ITAQUI
8715	ITATIBA DO SUL
8717	IVOTI
8719	JACUTINGA
8721	JAGUARAO
8723	JAGUARI
8725	JULIO DE CASTILHOS
8727	LAGOA VERMELHA
8729	LAJEADO
8731	LAVRAS DO SUL
8733	LIBERATO SALZANO
8735	MACHADINHO
8737	MARAU
8739	MARCELINO RAMOS
8741	MARIANO MORO
8743	MATA
8745	MAXIMILIANO DE ALMEIDA
8747	MIRAGUAI
8749	MONTENEGRO
8751	MOSTARDAS
8753	MUCUM
8755	NAO-ME-TOQUE
8757	NONOAI
8759	NOVA ARACA
8761	NOVA BASSANO
8763	NOVA BRESCIA
8765	NOVA PALMA
8767	NOVA PETROPOLIS
8769	NOVA PRATA
8771	NOVO HAMBURGO
8773	OSORIO
8775	PAIM FILHO
8777	PALMEIRA DAS MISSOES
8779	PALMITINHO
8781	PANAMBI
8783	PARAI
8785	PASSO FUNDO
8787	PEDRO OSORIO
8789	PEJUCARA
8791	PELOTAS
8793	PINHEIRO MACHADO
8795	PIRATINI
8797	PLANALTO
8799	PORTAO
8801	PORTO ALEGRE
8803	PORTO LUCENA
8805	PORTO XAVIER
8807	PUTINGA
8809	QUARAI
8811	REDENTORA
8813	RESTINGA SECA
8815	RIO GRANDE
8817	RIO PARDO
8819	ROCA SALES
8821	RODEIO BONITO
8823	ROLANTE
8825	RONDA ALTA
8827	RONDINHA
8829	ROQUE GONZALES
8831	ROSARIO DO SUL
8833	SALVADOR DO SUL
8835	SANANDUVA
8837	SANTA BARBARA DO SUL
8839	SANTA CRUZ DO SUL
8841	SANTA MARIA
8843	SANTANA DA BOA VISTA
8845	SANTANA DO LIVRAMENTO
8847	SANTA ROSA
8849	SANTA VITORIA DO PALMAR
8851	SANTIAGO
8853	SANTO ANGELO
8855	SANTO ANTONIO DA PATRULHA
8857	SANTO ANTONIO DAS MISSOES
8859	SANTO AUGUSTO
8861	SANTO CRISTO
8863	SAO BORJA
8865	SAO FRANCISCO DE ASSIS
8867	SAO FRANCISCO DE PAULA
8869	SAO GABRIEL
8871	SAO JERONIMO
8873	SAO JOSE DO NORTE
8875	SAO JOSE DO OURO
8877	SAO LEOPOLDO
8879	SAO LOURENCO DO SUL
8881	SAO LUIZ GONZAGA
8883	SAO MARCOS
8885	SAO MARTINHO
8887	SAO NICOLAU
8889	SAO PAULO DAS MISSOES
8891	SAO PEDRO DO SUL
8893	SAO SEBASTIAO DO CAI
8895	SAO SEPE
8897	SAO VALENTIM
8899	SAPIRANGA
8901	SAPUCAIA DO SUL
8903	SARANDI
8905	SEBERI
8907	SELBACH
8909	SERAFINA CORREA
8911	SERTAO
8913	SEVERIANO DE ALMEIDA
8915	CAPAO DA CANOA
8917	SOBRADINHO
8919	SOLEDADE
8921	TAPEJARA
8923	TAPERA
8925	TAPES
8927	TAQUARA
8929	TAQUARI
8931	TENENTE PORTELA
8933	TORRES
8935	TRAMANDAI
8937	TRES COROAS
8939	TRES DE MAIO
8941	TRES PASSOS
8943	TRIUNFO
8945	TUCUNDUVA
8947	TUPANCIRETA
8949	TUPARENDI
8951	URUGUAIANA
8953	VACARIA
8955	VENANCIO AIRES
8957	VERA CRUZ
8959	VERANOPOLIS
8961	VIADUTOS
8963	VIAMAO
8965	VICENTE DUTRA
8967	PALMARES DO SUL
8969	VICTOR GRAEFF
8971	TAVARES
8973	CAPAO DO LEAO
8975	SALTO DO JACUI
8977	COTIPORA
8979	COLIDER
8981	NOVA BRASILANDIA
8983	PARANATINGA
8985	SINOP
8987	ALTA FLORESTA
8989	ARAPUTANGA
8991	JAURU
8993	SAO JOSE DOS QUATRO MARCOS
8995	RIO BRANCO
8997	SALTO DO CEU
8999	PONTES E LACERDA
9001	ACORIZAL
9003	AGUA CLARA
9005	ALTO ARAGUAIA
9007	ALTO GARCAS
9009	ALTO PARAGUAI
9011	AMAMBAI
9013	ANASTACIO
9015	ANAURILANDIA
9017	ANTONIO JOAO
9019	APARECIDA DO TABOADO
9021	AQUIDAUANA
9023	ARAGUAINHA
9025	ARENAPOLIS
9027	ARIPUANA
9029	BANDEIRANTES
9031	BARAO DE MELGACO
9033	BARRA DO BUGRES
9035	BARRA DO GARCAS
9037	BATAGUASSU
9039	BATAYPORA
9041	BELA VISTA
9043	BONITO
9045	BRASILANDIA
9047	CACERES
9049	CAMAPUA
9051	CAMPO GRANDE
9053	CARACOL
9055	CAARAPO
9057	CASSILANDIA
9059	CHAPADA DOS GUIMARAES
9061	CORGUINHO
9063	CORUMBA
9065	COXIM
9067	CUIABA
9069	DIAMANTINO
9071	DOM AQUINO
9073	DOURADOS
9075	FATIMA DO SUL
9077	GENERAL CARNEIRO
9079	GLORIA DE DOURADOS
9081	GUIA LOPES DA LAGUNA
9083	GUIRATINGA
9085	IGUATEMI
9087	INOCENCIA
9089	ITAPORA
9091	ITIQUIRA
9093	IVINHEMA
9095	JACIARA
9097	JARAGUARI
9099	JARDIM
9101	JATEI
9103	LADARIO
9105	LUCIARA
9107	MARACAJU
9109	VILA BELA DA SANTISSIMA TRINDADE
9111	MIRANDA
9113	NAVIRAI
9115	NIOAQUE
9117	NOBRES
9119	NORTELANDIA
9121	NOSSA SENHORA DO LIVRAMENTO
9123	NOVA ANDRADINA
9125	PARANAIBA
9127	PEDRO GOMES
9129	POCONE
9131	PONTA PORA
9133	PONTE BRANCA
9135	PORTO DOS GAUCHOS
9137	PORTO MURTINHO
9139	POXOREU
9141	RIBAS DO RIO PARDO
9143	RIO BRILHANTE
9145	RIO NEGRO
9147	RIO VERDE DE MATO GROSSO
9149	ROCHEDO
9151	RONDONOPOLIS
9153	ROSARIO OESTE
9155	SANTO ANTONIO DO LEVERGER
9157	SIDROLANDIA
9159	TERENOS
9161	TESOURO
9163	TORIXOREU
9165	TRES LAGOAS
9167	VARZEA GRANDE
9169	ANGELICA
9171	ARAL MOREIRA
9173	ELDORADO
9175	DEODAPOLIS
9177	MIRASSOL D'OESTE
9179	MUNDO NOVO
9181	PEDRA PRETA
9183	SAO FELIX DO ARAGUAIA
9185	TANGARA DA SERRA
9187	VICENTINA
9189	JUSCIMEIRA
9191	AGUA BOA
9193	CANARANA
9195	NOVA XAVANTINA
9197	SANTA TEREZINHA
9199	SAO JOSE DO RIO CLARO
9201	ABADIANIA
9203	AGUA LIMPA
9205	ALEXANIA
9207	ALMAS
9209	ALOANDIA
9211	ALTO PARAISO DE GOIAS
9213	ALVORADA
9215	ALVORADA DO NORTE
9217	AMORINOPOLIS
9219	ANANAS
9221	ANAPOLIS
9223	ANHANGUERA
9225	ANICUNS
9227	APARECIDA DE GOIANIA
9229	APORE
9231	ARACU
9233	ARAGARCAS
9235	ARAGOIANIA
9237	ARAGUACEMA
9239	ARAGUACU
9241	ARAGUAINA
9243	ARAGUATINS
9245	ARAPOEMA
9247	ARRAIAS
9249	ARUANA
9251	AURILANDIA
9253	AURORA DO TOCANTINS
9255	AVELINOPOLIS
9257	AXIXA DO TOCANTINS
9259	BABACULANDIA
9261	BALIZA
9263	BARRO ALTO
9265	BELA VISTA DE GOIAS
9267	BOM JARDIM DE GOIAS
9269	BOM JESUS
9271	BRAZABRANTES
9273	BREJINHO DE NAZARE
9275	BRITANIA
9277	BURITI ALEGRE
9279	CABECEIRAS
9281	CACHOEIRA ALTA
9283	CACHOEIRA DE GOIAS
9285	CACU
9287	CAIAPONIA
9289	CALDAS NOVAS
9291	CAMPESTRE DE GOIAS
9293	CAMPINORTE
9295	CAMPO ALEGRE DE GOIAS
9297	CAMPOS BELOS
9299	CARMO DO RIO VERDE
9301	CATALAO
9303	CATURAI
9305	CAVALCANTE
9307	CERES
9309	DIVINOPOLIS DE GOIAS
9311	COLINAS DO TOCANTINS
9313	CONCEICAO DO TOCANTINS
9315	CORREGO DO OURO
9317	CORUMBA DE GOIAS
9319	CORUMBAIBA
9321	COUTO DE MAGALHAES
9323	CRISTALANDIA
9325	CRISTALINA
9327	CRISTIANOPOLIS
9329	CRIXAS
9331	CROMINIA
9333	CUMARI
9335	DAMIANOPOLIS
9337	DAMOLANDIA
9339	DAVINOPOLIS
9341	DIANOPOLIS
9343	DIORAMA
9345	DOIS IRMAOS DO TOCANTINS
9347	DUERE
9349	EDEIA
9351	ESTRELA DO NORTE
9353	FAZENDA NOVA
9355	FILADELFIA
9357	FIRMINOPOLIS
9359	FLORES DE GOIAS
9361	FORMOSA
9363	FORMOSO
9365	FORMOSO DO ARAGUAIA
9367	GOIANAPOLIS
9369	GOIANDIRA
9371	GOIANESIA
9373	GOIANIA
9375	GOIANIRA
9377	GOIAS
9379	GOIATUBA
9381	GUAPO
9383	GUARANI DE GOIAS
9385	GURUPI
9387	HEITORAI
9389	HIDROLANDIA
9391	HIDROLINA
9393	IACIARA
9395	INHUMAS
9397	IPAMERI
9399	IPORA
9401	ISRAELANDIA
9403	ITABERAI
9405	ITACAJA
9407	ITAGUARU
9409	ITAGUATINS
9411	ITAJA
9413	ITAPACI
9415	ITAPIRAPUA
9417	ITAPORA DO TOCANTINS
9419	ITAPURANGA
9421	ITARUMA
9423	ITAUCU
9425	ITUMBIARA
9427	IVOLANDIA
9429	JANDAIA
9431	JARAGUA
9433	JATAI
9435	JAUPACI
9437	JOVIANIA
9439	JUSSARA
9441	ALIANCA DO TOCANTINS
9443	LEOPOLDO DE BULHOES
9445	LUZIANIA
9447	MAIRIPOTABA
9449	MAMBAI
9451	MARA ROSA
9453	MARZAGAO
9455	PARANAIGUARA
9457	MAURILANDIA
9459	MINEIROS
9461	MIRACEMA DO TOCANTINS
9463	MIRANORTE
9465	MOIPORA
9467	MONTE ALEGRE DE GOIAS
9469	MONTE DO CARMO
9471	MONTES CLAROS DE GOIAS
9473	MORRINHOS
9475	MOSSAMEDES
9477	MOZARLANDIA
9479	MUTUNOPOLIS
9481	NATIVIDADE
9483	NAZARE
9485	NAZARIO
9487	NEROPOLIS
9489	NIQUELANDIA
9491	NOVA AMERICA
9493	NOVA AURORA
9495	NOVA ROMA
9497	NOVA VENEZA
9499	NOVO ACORDO
9501	NOVO BRASIL
9503	ORIZONA
9505	OURO VERDE DE GOIAS
9507	OUVIDOR
9509	PADRE BERNARDO
9511	PALMEIRAS DE GOIAS
9513	PALMELO
9515	PALMINOPOLIS
9517	PANAMA
9519	PARAISO DO TOCANTINS
9521	PARANA
9523	PARAUNA
9525	PEDRO AFONSO
9527	PEIXE
9529	COLMEIA
9531	PETROLINA DE GOIAS
9533	GOIATINS
9535	PILAR DE GOIAS
9537	PINDORAMA DO TOCANTINS
9539	PIRACANJUBA
9541	PIRANHAS
9543	PIRENOPOLIS
9545	PIRES DO RIO
9547	PIUM
9549	PONTALINA
9551	PONTE ALTA DO BOM JESUS
9553	PONTE ALTA DO TOCANTINS
9555	PORANGATU
9557	PORTELANDIA
9559	PORTO NACIONAL
9561	POSSE
9563	QUIRINOPOLIS
9565	RIALMA
9567	RIANAPOLIS
9569	LIZARDA
9571	RIO VERDE
9573	RUBIATABA
9575	SANCLERLANDIA
9577	SANTA BARBARA DE GOIAS
9579	SANTA CRUZ DE GOIAS
9581	SANTA HELENA DE GOIAS
9583	SANTA RITA DO ARAGUAIA
9585	SANTA ROSA DE GOIAS
9587	SANTA TEREZA DE GOIAS
9589	SANTA TEREZINHA DE GOIAS
9591	SAO DOMINGOS
9593	SAO FRANCISCO DE GOIAS
9595	PLANALTINA
9597	SAO JOAO D'ALIANCA
9599	SAO LUIS DE MONTES BELOS
9601	SAO MIGUEL DO ARAGUAIA
9603	SAO SEBASTIAO DO TOCANTINS
9605	SAO SIMAO
9607	SERRANOPOLIS
9609	SILVANIA
9611	SITIO D'ABADIA
9613	SITIO NOVO DO TOCANTINS
9615	TAGUATINGA
9617	TAQUARAL DE GOIAS
9619	TOCANTINIA
9621	TOCANTINOPOLIS
9623	TRES RANCHOS
9625	TRINDADE
9627	GUARAI
9629	PRESIDENTE KENNEDY
9631	TURVANIA
9633	URUACU
9635	URUANA
9637	URUTAI
9639	VARJAO
9641	VIANOPOLIS
9643	XAMBIOA
9645	ACREUNA
9647	MINACU
9649	PALMEIROPOLIS
9651	MUNDO NOVO
9653	NOVA CRIXAS
9655	NOVA GLORIA
9657	VICENTINOPOLIS
9659	SILVANOPOLIS
9661	AMERICANO DO BRASIL
9663	NOVA OLINDA
9665	WANDERLANDIA
9667	FIGUEIROPOLIS
9669	ARAGUAPAZ
9671	ARENOPOLIS
9673	CACHOEIRA DOURADA
9675	DOVERLANDIA
9677	SANTO ANTONIO DO DESCOBERTO
9679	RIO SONO
9681	INDIARA
9683	FATIMA
9685	AUGUSTINOPOLIS
9687	CAMPINACU
9689	SANTA ISABEL
9691	SAO VALERIO DA NATIVIDADE
9693	BARROLANDIA
9695	BERNARDO SAYAO
9697	COMBINADO
9699	GOIANORTE
9701	BRASILIA
9703	NOVO ALEGRE
9705	PEQUIZEIRO
9707	EXTERIOR
9711	MARIANOPOLIS DO TOCANTINS
9713	APARECIDA DO RIO NEGRO
9715	BURITI DO TOCANTINS
9717	CASEARA
9719	DIVINOPOLIS DO TOCANTINS
9721	NOVA ROSALANDIA
9723	PORTO ALEGRE DO TOCANTINS
9725	PRAIA NORTE
9727	SAMPAIO
9729	SANTA ROSA DO TOCANTINS
9731	SANTA TEREZA DO TOCANTINS
9733	PALMAS
9735	NOVO PLANALTO
9737	PALESTINA DE GOIAS
9739	PARANHOS
9741	RIBEIRAO CASCALHEIRA
9743	SANTA FE DE GOIAS
9745	SANTA RITA DO PARDO
9747	SAO JOAO DA PARAUNA
9749	SAO LUIZ DO NORTE
9751	SAO MIGUEL DO PASSA QUATRO
9753	SENADOR CANEDO
9755	SIMOLANDIA
9757	SONORA
9759	TERESINA DE GOIAS
9761	TROMBAS
9763	TAPURAH
9765	TURVELANDIA
9767	ALAGOINHA DO PIAUI
9769	ADELANDIA
9771	AGUA FRIA DE GOIAS
9773	APIACAS
9775	BONFINOPOLIS
9777	CAMPO NOVO DO PARECIS
9779	CAMPO VERDE
9781	CAMPOS VERDES
9783	CASTANHEIRA
9785	CEZARINA
9787	CHAPADAO DO SUL
9789	CLAUDIA
9791	COLINAS DO SUL
9793	DOIS IRMAOS DO BURITI
9795	EDEALINA
9797	FAINA
9799	GOUVELANDIA
9801	BODOQUENA
9803	COSTA RICA
9805	DOURADINA
9807	ITAQUIRAI
9809	SAO GABRIEL DO OESTE
9811	SELVIRIA
9813	SETE QUEDAS
9815	TACURU
9817	TAQUARUSSU
9819	JUARA
9821	TEUTONIA
9823	BOM PRINCIPIO
9825	PAROBE
9827	FORTALEZA DOS VALOS
9829	JOIA
9831	JUINA
9833	DENISE
9835	IRANDUBA
9837	ITAMARATI
9839	MANAQUIRI
9841	PRESIDENTE FIGUEIREDO
9843	RIO PRETO DA EVA
9845	SAO SEBASTIAO DO UATUMA
9847	TABATINGA
9849	UARINI
9851	TONANTINS
9853	QUIXELO
9855	UMIRIM
9857	VARJOTA
9859	JABORANDI
9861	JANGADA
9863	CAMPINAPOLIS
9865	COCALINHO
9867	NOVO SAO JOAQUIM
9869	ARAGUAIANA
9871	PRIMAVERA DO LESTE
9873	BRASNORTE
9875	PORTO ESPERIDIAO
9877	INDIAVAI
9879	RESERVA DO CABACAL
9881	FIGUEIROPOLIS D'OESTE
9883	COMODORO
9885	PARANAITA
9887	GUARANTA DO NORTE
9889	NOVA CANAA DO NORTE
9891	PEIXOTO DE AZEVEDO
9893	NOVA OLIMPIA
9895	PORTO ALEGRE DO NORTE
9897	VILA RICA
9899	MARCELANDIA
9901	ITAUBA
9903	NOVO HORIZONTE DO NORTE
9905	VERA
9907	SORRISO
9909	TERRA NOVA DO NORTE
9911	ALTO TAQUARI
9913	NOVA TEBAS
9915	DIAMANTE D'OESTE
9917	QUITERIANOPOLIS
9919	ITAGUARI
9921	JURUENA
9923	JUTI
9925	LUCAS DO RIO VERDE
9927	MATRINCHA
9929	MATUPA
9931	MIMOSO DE GOIAS
9933	MONTIVIDIU
9935	MORRO AGUDO DE GOIAS
9937	NOVA MUTUM
9939	ABDON BATISTA
9941	APIUNA
9943	CELSO RAMOS
9945	DOUTOR PEDRINHO
9947	GODOY MOREIRA
9949	IBEMA
9951	IPORA DO OESTE
9953	IRACEMINHA
9955	IVATE
9957	JOSE BOITEUX
9959	LINDOESTE
9961	LINDOIA DO SUL
9963	MAREMA
9965	OURO VERDE DO OESTE
9967	SANTA ROSA DO SUL
9969	SANTA TEREZA DO OESTE
9971	TIMBO GRANDE
9973	UNIAO DO OESTE
9975	URUPEMA
9977	VITOR MEIRELES
9979	BOM SUCESSO DO SUL
9981	HONORIO SERPA
9983	FAZENDA RIO GRANDE
9985	ITAPOA
9989	SERRA ALTA
9991	TUNAPOLIS
9993	GUARINOS
9995	RIO QUENTE
9997	CORONEL SAPUCAIA
\.


--
-- Data for Name: natju; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.natju (codigo, descricao) FROM stdin;
\.


--
-- Data for Name: pais; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.pais (codigo, descricao) FROM stdin;
0	COLIS POSTAUX
13	AFEGANISTAO
17	ALBANIA
20	ALBORAN-PEREJIL,ILHAS
23	ALEMANHA
25	ALEMANHA, REP. DEMOCRATICA DA
31	BURKINA FASO
37	ANDORRA
40	ANGOLA
41	ANGUILLA
43	ANTIGUA E BARBUDA
47	ANTILHAS HOLANDESAS
53	ARABIA SAUDITA
59	ARGELIA
63	ARGENTINA
64	ARMENIA, REPUBLICA DA
65	ARUBA
69	AUSTRALIA
72	AUSTRIA
73	AZERBAIJAO, REPUBLICA DO
77	BAHAMAS
80	Bahrein, Ilhas
81	BANGLADESH
83	BARBADOS
85	BIELO-RUSSIA (BELARUS) REP. DA
87	BELGICA
88	BELISE
90	BERMUDAS
93	Mianmar (Birmânia)
97	BOLIVIA
98	Bosnia-Herzegovina (Republica da)
100	ZONA FRANCA DE MANAUS
101	BOTSUANA
105	BRASIL
106	BRASIL (AFRETAMENTO)
108	BRUNEI
111	BULGARIA
115	BURUNDI
119	BUTAO
127	Cabo Verde,República de
131	CACHEMIRA
137	CAYMAN,ILHAS
141	CAMBOJA
145	CAMAROES
149	CANADA
152	CANAL (ILHAS NORMANDAS)
153	CASAQUISTAO, REPUBLICA DO
154	CATAR
158	CHILE
160	China, República Popular
161	FORMOSA (PROVINCIA DA CHINA)
163	CHIPRE
165	COCOS (KEELING),ILHAS
169	COLOMBIA
173	COMORES, ILHAS
177	CONGO
183	COOK, ILHAS
187	Coréia, Rep.Pop.Democrática
190	COREIA REPUBLICA DA
193	COSTA DO MARFIM
195	CROACIA, REPUBLICA DA
196	COSTA RICA
198	COVEITE
199	CUBA
229	BENIN
232	DINAMARCA
235	DOMINICA
237	DUBAI
239	EQUADOR
240	EGITO
244	EMIRADOS ARABES UNIDOS
245	ESPANHA
246	ESLOVENIA, REPUBLICA DA
247	ESLOVACA, REPUBLICA
249	ESTADOS UNIDOS
251	ESTONIA, REPUBLICA DA
253	ETIOPIA
255	FALKLAND (ILHAS MALVINAS)
259	FEROE, ILHAS
263	FEZZAN
267	FILIPINAS
271	FINLANDIA
275	FRANCA
281	GABAO
285	GAMBIA
289	GANA
291	GEORGIA, REPUBLICA DA
293	GIBRALTAR
297	GRANADA
301	GRECIA
305	GROENLANDIA
309	GUADALUPE
313	GUAM
317	GUATEMALA
325	GUIANA FRANCESA
329	GUINE, REPUBLICA DA
331	GUINE-EQUATORIAL
334	GUINE BISSAU
337	GUIANA
341	HAITI
345	HONDURAS
351	HONG-KONG
355	HUNGRIA
357	IEMEN, REPUBLICA DO
358	IEMEN DEMOCRATICO
361	INDIA
365	INDONESIA
369	IRAQUE
372	Irã, República Islamica do
375	IRLANDA
379	ISLANDIA
383	ISRAEL
386	ITALIA
388	Sérvia E Montenegro(Iugoslávia,Rep. Fede
391	JAMAICA
395	JAMMU
399	JAPAO
403	JORDANIA
411	KIRIBATI
420	LAOS, REP. POP. E DEMOCR. DO
423	LEBUAN(ILHA)
426	LESOTO
427	LETONIA, REPUBLICA DA
431	LIBANO
434	LIBERIA
438	LIBIA
440	LIECHTENSTEIN
442	LITUANIA, REPUBLICA DA
445	LUXEMBURGO
447	MACAU
450	MADAGASCAR
455	MALAISIA
458	MALAVI
461	MALDIVAS
464	MALI
467	MALTA
472	MARIANAS DO NORTE
474	MARROCOS
476	MARSHALL, ILHA
477	MARTINICA
485	MAURICIO
488	MAURITANIA
493	MEXICO
494	MOLDAVIA (MOLDAVA),REP. DA
495	MONACO
497	MONGOLIA
499	MICRONESIA, EST.FED.DA
501	MONSERRAT
505	MOCAMBIQUE
507	NAMIBIA
508	NAURU
511	Christmas,Ilhas (Navidad)
517	NEPAL
521	NICARAGUA
525	NIGER
528	NIGERIA
531	NIUE
535	NORFOLK, ILHA
538	NORUEGA
542	NOVA CALEDONIA
545	PAPUA NOVA GUINE
548	NOVA ZELANDIA
551	VANUATU
556	OMA
563	Pacífico, Ilhas do (Administ.dos Eua)
566	Pacífico, Ilhas do
569	PACIF. ILHAS TERR. USA
573	Países Baixos (Holanda)
575	PALAU, REPUBLICA DO
576	PAQUISTAO
580	PANAMA
583	PAPUA, TERRITORIO DE
586	PARAGUAI
589	PERU
593	PITCAIRN, ILHA DE
599	POLINESIA FRANCESA
603	POLONIA
607	PORTUGAL
611	PORTO RICO
623	QUENIA
625	QUIRGUIZIA, REPUBLICA DA
628	REINO UNIDO
640	REPUBLICA CENTRO AFRICANA
647	REPUBLICA DOMINICANA
660	REUNIAO
665	ZIMBABUE
666	COMUNIDADE ECONOMICA EUROPEIA
670	ROMENIA
675	RUANDA
676	RUSSIA, FEDERACAO DA
677	SALOMAO, ILHAS
685	SAARA OCIDENTAL
687	EL SALVADOR
690	SAMOA
691	SOMOA AMERICANA
695	SAO CRISTOVAO E NEVES
697	SAN MARINO
700	SAO PEDRO E MIQUELLON
705	SAO VICENTE E GRANADINAS
710	SANTA HELENA
715	SANTA LUCIA
720	SAO TOME E PRINCIPE
728	SENEGAL
731	SEYCHELLES
735	SERRA LEOA
738	SIKKIM
741	CINGAPURA
744	SIRIA, REP. ARABE DA
748	SOMALIA
750	SRI-LANKA
754	SUAZILANDIA
756	AFRICA DO SUL
759	SUDAO
764	SUECIA
767	SUICA
770	SURINAME
772	TADJIQUISTAO, REPUBLICA DO
776	TAILANDIA
780	TANZANIA
782	Território Britânico no Oceano Índico
783	DJIBUTI
785	TERR. ALTA COMISS. PAC. OCEAN.
788	CHADE
790	TCHECOSLOVAQUIA
791	THECA, REPUBLICA
795	TIMOR ORIENTAL
800	TOGO
805	TOQUELAU
810	TONGA
815	TRINIDAD E TOBAGO
820	TUNISIA
823	TURCAS E CAICOS, ILHAS
824	Turcomenistão, República do
827	TURQUIA
828	TUVALU
831	UCRANIA
833	UGANDA
840	U.R.S.S.
845	URUGUAI
847	UZBEQUISTAO, REPUBLICA DO
848	VATICANO, CIDADE DO (SANTA SE)
850	VENEZUELA
855	VIETNAME DO NORTE
858	VIETNA
863	VIRGENS, ILHAS (BRITANICAS)
866	VIRGENS, ILHAS (EUA)
870	FIJI
875	WALLIS E FUTURNA, ILHAS
888	ZAIRE
890	ZAMBIA
895	ZONA DO CANAL DO PANAMA
990	PROV. DE NAVIOS E AERONAVES
997	NAO DECLARADOS
998	NAO DECLARADO PRELIMINAR
999	NAO DECLARADOS
\.


--
-- Data for Name: quals; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.quals (codigo, descricao) FROM stdin;
0	Não informada
5	Administrador
8	Conselheiro de Administração
9	Curador
10	Diretor
11	Interventor
12	Inventariante
13	Liquidante
14	Mãe
15	Pai
16	Presidente
17	Procurador
18	Secretário
19	Síndico (Condomínio)
20	Sociedade Consorciada
21	Sociedade Filiada
22	Sócio
23	Sócio Capitalista
24	Sócio Comanditado
25	Sócio Comanditário
26	Sócio de Indústria
28	Sócio-Gerente
29	Sócio Incapaz ou Relat.Incapaz (exceto menor)
30	Sócio Menor (Assistido/Representado)
31	Sócio Ostensivo
32	Tabelião
33	Tesoureiro
34	Titular de Empresa Individual Imobiliária
35	Tutor
37	Sócio Pessoa Jurídica Domiciliado no Exterior
38	Sócio Pessoa Física Residente no Exterior
39	Diplomata
40	Cônsul
41	Representante de Organização Internacional
42	Oficial de Registro
43	Responsável
46	Ministro de Estado das Relações Exteriores
47	Sócio Pessoa Física Residente no Brasil
48	Sócio Pessoa Jurídica Domiciliado no Brasil
49	Sócio-Administrador
50	Empresário
51	Candidato a cargo Político Eletivo
52	Sócio com Capital
53	Sócio sem Capital
54	Fundador
55	Sócio Comanditado Residente no Exterior
56	Sócio Comanditário Pessoa Física Residente no Exterior
57	Sócio Comanditário Pessoa Jurídica Domiciliado no Exterior
58	Sócio Comanditário Incapaz
59	Produtor Rural
60	Cônsul Honorário
61	Responsável indígena
62	Representante da Instituição Extraterritorial
63	Cotas em Tesouraria
64	Administrador Judicial
65	Titular Pessoa Física Residente ou Domiciliado no Brasil
66	Titular Pessoa Física Residente ou Domiciliado no Exterior
67	Titular Pessoa Física Incapaz ou Relativamente Incapaz (exceto menor)
68	Titular Pessoa Física Menor (Assistido/Representado)
69	Beneficiário Final
70	Administrador Residente ou Domiciliado no Exterior
71	Conselheiro de Administração Residente ou Domiciliado no Exterior
72	Diretor Residente ou Domiciliado no Exterior
73	Presidente Residente ou Domiciliado no Exterior
74	Sócio-Administrador Residente ou Domiciliado no Exterior
75	Fundador Residente ou Domiciliado no Exterior
78	Titular Pessoa Jurídica Domiciliada no Brasil
79	Titular Pessoa Jurídica Domiciliada no Exterior
\.


--
-- Data for Name: simples; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.simples (cnpj_basico, opcao_pelo_simples, data_opcao_simples, data_exclusao_simples, opcao_mei, data_opcao_mei, data_exclusao_mei) FROM stdin;
41273593	N	20210318	20210929	N	20210318	20210929
41273594	S	20210318	0	S	20210318	0
41273595	S	20210318	0	S	20210318	0
41273596	N	20210318	20220630	N	20210318	20220630
41273597	S	20210318	0	S	20210318	0
\.


--
-- Data for Name: socios; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.socios (cnpj_basico, identificador_socio, nome_socio_razao_social, cpf_cnpj_socio, qualificacao_socio, data_entrada_sociedade, pais, representante_legal, nome_do_representante, qualificacao_representante_legal, faixa_etaria) FROM stdin;
\.


--
-- Name: audit audit_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.audit
    ADD CONSTRAINT audit_pkey PRIMARY KEY (audi_id);


--
-- Name: natju natju_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.natju
    ADD CONSTRAINT natju_pkey PRIMARY KEY (codigo);


--
-- Name: cnae_codigo_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX cnae_codigo_idx ON public.cnae USING btree (codigo);


--
-- Name: empresa_cnpj_basico; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX empresa_cnpj_basico ON public.empresa USING btree (cnpj_basico);


--
-- Name: estabelecimento_cep; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX estabelecimento_cep ON public.estabelecimento USING btree (cep);


--
-- Name: estabelecimento_cnpj_dv; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX estabelecimento_cnpj_dv ON public.estabelecimento USING btree (cnpj_dv);


--
-- Name: estabelecimento_cnpj_ordem; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX estabelecimento_cnpj_ordem ON public.estabelecimento USING btree (cnpj_ordem);


--
-- Name: estabelecimento_uf; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX estabelecimento_uf ON public.estabelecimento USING btree (uf);


--
-- Name: moti_codigo_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX moti_codigo_idx ON public.moti USING btree (codigo);


--
-- Name: munic_codigo_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX munic_codigo_idx ON public.munic USING btree (codigo);


--
-- Name: natju_codigo_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX natju_codigo_idx ON public.natju USING btree (codigo);


--
-- Name: pais_codigo_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX pais_codigo_idx ON public.pais USING btree (codigo);


--
-- Name: socios_cnpj_basico; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX socios_cnpj_basico ON public.socios USING btree (cnpj_basico);


--
-- Name: TABLE audit; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.audit TO postgres;


--
-- Name: TABLE cnae; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.cnae TO postgres;


--
-- Name: TABLE empresa; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.empresa TO postgres;


--
-- Name: TABLE estabelecimento; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.estabelecimento TO postgres;


--
-- Name: TABLE moti; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.moti TO postgres;


--
-- Name: TABLE munic; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.munic TO postgres;


--
-- Name: TABLE natju; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.natju TO postgres;


--
-- Name: TABLE pais; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.pais TO postgres;


--
-- Name: TABLE quals; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.quals TO postgres;


--
-- Name: TABLE simples; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.simples TO postgres;


--
-- Name: TABLE socios; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.socios TO postgres;


--
-- PostgreSQL database dump complete
--


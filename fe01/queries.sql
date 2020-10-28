-- a) Quantos títulos possui a coleção?

select count(*) from titulo;

-- b) Quantas músicas no total possui toda a coleção?

select count(*) from musica;

-- c) Quantos autores existem na coleção?

select count(*) from autor;

-- d) Quantas editoras distintas existem na coleção?
select count(distinct(e.id_editora)) from editora e;

-- e) O autor "Max Changmin" é o principal autor de quantos títulos?

select count(*) from autor join titulo on autor.id_autor = titulo.id_autor where nome='Max Changmin';

-- f) No ano de 1970, quais foram os títulos comprados pelo utilizador?

select titulo from titulo where extract(year from dta_compra)='1970';

-- g) Qual o autor do título que foi adquirido em “01-02-2010”, cujo preço foi de 12€?

select 
    a.nome
from
    titulo t
join autor a
on t.id_autor = a.id_autor
and t.dta_compra = to_date('01-02-2010', 'dd-mm-yyyy')
and t.preco = 12;

-- h) Na alínea anterior indique qual a editora desse título?

select 
    e.nome
from
    titulo t
join autor a
on t.id_autor = a.id_autor
join editora e
on t.id_editora = e.id_editora
and t.dta_compra = to_date('01-02-2010', 'dd-mm-yyyy')
and t.preco = 12;

-- i) Quais as reviews (data e classificação) existentes para o título "oh whoa oh"?

select dta_review,conteudo from review join titulo on review.ID_TITULO=titulo.ID_TITULO where titulo='oh whoa oh';

-- j) Quais as reviews (data e classificação) existentes para o título “pump”, ordenadas por data da mais antiga

select
    t.titulo, r.dta_review, r.conteudo
from review r
join titulo t
on r.id_titulo = t.id_titulo
and t.titulo = 'pump'
order by r.dta_review asc;

-- k) Quais os diversos autores das músicas do título lançado a ‘04-04-1970’ com o preço de 20€?

select 
    a.nome, t.titulo, t.dta_compra, t.preco
from autor a
join titulo t on t.id_autor = a.id_autor
where t.dta_compra = to_date('04-04-1970', 'dd-mm-yy')
and t.preco = 20;

-- l) Qual foi o total de dinheiro investido em compras de título da editora ‘EMI’?

select sum(t.preco) as Preco_Investido
from titulo t, editora e
where t.id_editora = e.id_editora and e.nome = 'EMI';

-- m)  Qual o título mais antigo cujo preço foi de 20€?

select t.TITULO from TITULO t
where t.PRECO = 20
order by t.DTA_COMPRA asc
fetch first 1 rows only;

-- n) Quantos “MP3” tem a coleção?

select count(*) from SUPORTE s 
inner join TITULO t
on s.ID_SUPORTE = t.ID_SUPORTE
where s.NOME = 'MP3';

-- o) Destes mp3 quais são o títulos cujo género é: Pop Rock?

select t.titulo 
from titulo t, suporte s, genero g
where t.id_suporte = s.id_suporte and t.id_genero = g.id_genero and s.nome = 'MP3' and g.nome = 'Pop Rock';

-- p) Qual o custo total com “Blue-Ray”?

select sum(t.PRECO) from SUPORTE s 
inner join TITULO t
on s.ID_SUPORTE = t.ID_SUPORTE
where s.NOME = 'Blue-Ray';

-- q) Qual o custo total com “Blue-Ray” cuja editora é a EMI?

select sum(t.preco) as Total 
from titulo t, suporte s, editora e 
where t.id_suporte = s.id_suporte and t.id_editora = e.id_editora and s.nome = 'Blue-Ray' and e.nome = 'EMI';

-- r)  Qual o património total dos títulos da coleção?

select sum(t.PRECO) as Patrimonio from TITULO t;

-- s) Qual a editora na qual o colecionador investiu mais dinheiro?

select e.nome as Nome,sum(t.preco) as Total
from titulo t, editora e 
where t.id_editora = e.id_editora
group by t.id_editora, e.nome
order by Total desc;

-- t) Qual a editora que possui mais títulos de “Heavy Metal” na coleção? Quanto titulo possui essa editora?
select e.nome as Editora, count(e.id_editora) as "Número de títulos" from titulo t 
inner join GENERO g
on g.ID_GENERO = t.ID_GENERO
inner join EDITORA e
on e.ID_EDITORA = t.ID_EDITORA
where g.nome = 'Heavy Metal'
group by e.nome
order by count(e.id_editora) desc
fetch first 1 rows only;

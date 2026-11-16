DATA = """
1|ok|El niño come una manzana
1|ok|La niña lee un libro
1|ok|Ana compra una casa
1|ok|Luis ve el perro
1|ok|El gato duerme
1|ok|Los niños comen unas manzanas
1|ok|Las niñas leen los libros
1|ok|El profesor compró la mesa
1|ok|La niña corrió
1|ok|Luis vio un gato
1|ok|Los perros durmieron
1|ok|El profesor lee un libro
1|ok|Ana come una manzana
1|ok|Los gatos corren
1|ok|Luis compró unos libros
1|ok|Las niñas vieron la casa
1|no|Los niño come una manzana
1|no|La niño lee un libro
1|no|El gato duermen
1|no|Ana comen una manzana
2|ok|El niño pequeño come una manzana roja
2|ok|La niña bonita lee un libro nuevo
2|ok|El perro grande corre rápidamente en el parque
2|ok|Ana compra una casa nueva para Luis
2|ok|Los gatos viejos duermen en la casa
2|ok|Luis lee un libro sobre la ciudad
2|ok|El profesor come una manzana en el parque hoy
2|ok|Las niñas pequeñas corrieron rápidamente
2|ok|Los profesores compraron unas mesas nuevas ayer
2|ok|La niña vio un perro pequeño con el niño
2|ok|Hoy el niño come una manzana
2|ok|El niño come mucho
2|ok|Luis duerme en la casa grande
2|ok|Las niñas leen unos libros grandes
2|no|El niño pequeña come una manzana
2|no|Los gatos viejo duermen en la casa
2|no|La niña bonita lee un libro nuevos
2|no|El perro grande corren en el parque
2|no|Una niñas compra una casa nueva
2|no|Los profesores compró unas mesas nuevas
3|ok|Los niños comen manzanas
3|ok|El niño que lee un libro corre
3|ok|Ana y Luis compran una casa
3|ok|El niño come una manzana y la niña lee un libro
3|ok|Ana quiere comprar una casa
3|ok|La casa del profesor es bonita
3|ok|Come una manzana
3|ok|Corren en el parque
3|ok|El niño la ve
3|ok|Ana dice que Luis duerme
3|ok|Ana ve el libro que compró Luis
3|ok|¿Quién compró la casa?
3|ok|El niño pequeño de la niña come una manzana
3|ok|La niña vio un perro con un libro
3|no|El gato duerme un libro
3|no|Luis corre la manzana
3|no|Niño el come manzana una
3|no|Los el niños comen
3|no|Ana come come una manzana
3|no|El niño duerme hoy hoy
"""
SET = [(int(n), g, s) for n, g, s in (l.split('|') for l in DATA.strip().splitlines())]
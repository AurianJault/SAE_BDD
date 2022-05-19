# SAE2.04 : Exploitation d'une base de donnée

## Info

Lien du csv : https://www.kaggle.com/datasets/nguyenngocphung/10000-amazon-products-dataset?resource=download  
Lien du doc : https://docs.google.com/document/d/13Vzunw1td49xJpwJos_GKfYhAmUG6cgKVLPSLH-zLqw/edit?usp=sharing
mdp de la bdd : haha  

## Table

### amazon

uniq_id  
product_name  
manufacturer  
price  
number_available_in_stock  
number_of_reviews  
number_of_answered_questions  
average_review_rating  
amazon_category_and_sub_category  
description  
product_information  
product_description  
items_customers_buy_after_viewing_this_item  
customer_questions_and_answers 

### detail

id
weight
hauteur
largeur
profondeur
assemblage
battery_Included
battery_needed
recommended_age
language

## Questions

* % de prod par manufactureur
* médiane des review
* Pourcentage des reviews 
  * Par tranche de note
  * Par manufactureur
  * Par catégorie
* % d'article avec dans la desc "Best"
* Stats relation entre vente et reponse aux questions
* prix max/min par catégories
* prix max/min par manufactureurs


## Stats :
manufacturer :
2% lego
2% disney
Autre

51 % 5/5 étoiles

## Changements
- [X] price -> cut £ signe
- [X] number_available_in_stock -> cut en deux partie + ajout d'une colonne
- [X] average_review_rating -> cut tout sauf le chiffre

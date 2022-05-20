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
product_information  

### detail
uniq_id
weight  
dimension
assembly   
battery_included  
battery_required  
recommended_age  
pas fait -> language

## Questions
* % de prod par manufactureur
* médiane des reviews
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
- [X] remove 2 weird lines
- [X] change value were price is >999

## Query
- Better note if battery is included when required [Rémi]
- Number of different products by a manufacturer [Bastien]
- Number of products available by manufacturer [Bastien] -> pas ouf
- Number of review by category [Bastien]
- Avg Price by category sort by rates [Bastien]
- Most reviewed products by recommanded age [Bastien] link with billel reco cat 4 age
- 
### Interpréteur mini langage 3A AL1 - Théorie des langages et compilation

---

### Fonctionnalitées :

1.Spécifications de la version minimale (8/20) :
- Votre interpréteur devra gérer les noms de variables à plusieurs caractères. 
- Gérer les instructions suivantes :
  - Affectation
  - Affichage d’expressions numériques (pouvant contenir des variables numériques) 
  - Instructions conditionnelles : implémenter le si-alors-sinon/si-alors 
  - Structures itératives : implémenter le while et le for 
  - Affichage de l’arbre de syntaxe (sur la console ou avec graphViz) 

2.Améliorations majeures :
- Gérer les fonctions avec / sans paramètre, sans valeur de retour 

3.Améliorations mineures :
- Gestion du type chaine de caractères
- Print multiples : print(x+2, « toto »);
- Incrémentation : x++
- Gestion des booléen : True/False

---
## Synthaxe

- opération arithmétiques ➔ test/file1.txt  
s1='print(((1+4)*4-10)/2);'


- affectation, print ➔ test/file2.txt  
s2='x=4;x=x+3;print(x);'
  

- incrémentation ➔ test/file3.txt    
s3='x=9; x++; print(x);'
  

- if, comparaison ➔ test/file4.txt   
s4='x=5; if x < 6 {print(6);}; if x < 4 {print(4);};'
  

- if-else ➔ test/file5.txt   
s5='x=5; if x < 10 {print(0);} else { print(10);};'


- while ➔ test/file6.txt   
s6=’x=0;while(x<30){x=x+3;print(x);};’


- for ➔ test/file7.txt  
s7='for(i=0; i<5; i=i+1){print(i*i);};'


- chaine de charactere, print multiple ➔ test/file8.txt   
s8='y="hello world"; print(y, 5+5, 4, "ok");'


- True, False ➔ test/file9.txt   
s9='print(1>2);print(2>1);'


- fonction sans paramètres ➔ test/file10.txt   
s10='function test() { ok="test"; print(ok); }; test();'


- fonction avec paramètres ➔ test/file11.txt   
s11='function test(x, y) { print(x); y=y+5; print(y);}; test(5, 5);'

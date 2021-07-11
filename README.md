Pour ce bot pas ouf, vous devez vous rendre dans le fichier config.

Les variables d'url doivent être encodées en base64.
Ainsi, imaginons que vous cherchiez un appartement à Rennes, 50m carré à moins de 200 euros :

l'url sera :
`https://www.leboncoin.fr/recherche?category=10&locations=Rennes__48.10980729840584_-1.6675040381352901_10000&real_estate_type=2&price=min-250&square=50-max` 

en b64 : `aHR0cHM6Ly93d3cubGVib25jb2luLmZyL3JlY2hlcmNoZT9jYXRlZ29yeT0xMCZsb2NhdGlvbnM9UmVubmVzX180OC4xMDk4MDcyOTg0MDU4NF8tMS42Njc1MDQwMzgxMzUyOTAxXzEwMDAwJnJlYWxfZXN0YXRlX3R5cGU9MiZwcmljZT1taW4tMjUwJnNxdWFyZT01MC1tYXg=`

Faites la même chose pour SeLoger et PAP.

Pour PAP il vous faudra ajouter une petite chose : une liste des villes. Car oui, pour PaP quand on cherche "Rennes" ca veut aussi dire "Paris" et "Marseille".
Séparez les d'une virgules et d'un espace `paris, paris`, pour connaitre le bon orthographe à mettre, faites une petite recherche sur PAP.fr d'un appartement et C/C la ville sur une annonce à Rennes, ça évitera une majuscule, accent ou n'importe quoi qui vous échaperait.

Puis ensuite, dans `receiver` et `receiver2` mettez votre email ainsi que l'email OPTIONNEL de votre ami/conjoint/plan cul, en espérant que vous ayez un plan cul plutôt qu'une relation sérieuse.

Bien, vous avez quasiment fini, il suffit désormais de mettre un email GMAIL (n'oubliez pas [d'activer le POP/imap](https://support.google.com/a/answer/105694) ) et votre MOT DE PASSE (bawé faut pas se foutre de ma gueule j'allais pas interfacer un truc propre et sécurisé avec les good practices).

Et enfin, mettez une date de fin d'execution pour le programme, réspectez le format de l'exemple par défaut.

Laissez ca mijoter et recevez chaque jour toute les nouvelles annonces fraichement scrap par le bot.

Il y a moyen que LBC et SeLoger changent 2-3 merdes sur le front de MERDE (vraiment, faut qu'ils engagent plus de stagiaire, c'est pas croyable), donc ne me prévenez pas et apprenez à scraper.

bye, des bisous, que dieu vous crache dessus.

# Documentation

## Go to 

Pour lancer un "go to" simple (sans odométrie):
```bash
python run_go_to_simple origin_x origin_y origin_theta target_x target_y target_theta
```

## Mapping (indirect)

Pour avoir un mapping après avoir fait un tracé, on lance la séquence d'enregistrement et on la kill (Ctrl + C) une fois fini:
```
python mapping_data.py
^C
```

Puis on lance le mapping :
```
python mapping.py
```
### Mapping et suivi de lignes.

Il est aussi possible de lancer un mapping lors du suivi des lignes en lançant : 
```run_line_following_map.py```



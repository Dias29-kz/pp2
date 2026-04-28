# TSIS3 Racer with Music

Ready-to-run Racer project with generated images and sounds.

## Structure

```text
TSIS3/
├── racer.py
├── README.md
└── assets/
    ├── images/
    │   ├── Road.jpg
    │   ├── main_car.jpg
    │   ├── NPC1.jpg ... NPC9.jpg
    │   ├── 1coin.jpg
    │   ├── 3coin.jpg
    │   └── 5coin.jpg
    └── sounds/
        ├── menu.wav
        ├── background.wav
        ├── coin.wav
        └── crash.wav
```

## Run

```bash
cd TSIS3
python3 racer.py
```

## Controls

- UP / DOWN: menu navigation
- LEFT / RIGHT: difficulty in menu
- ENTER: select
- A / D or LEFT / RIGHT: move car
- W / UP: gas
- S / DOWN: brake
- R: restart
- ESC: menu after game over

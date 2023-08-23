# LATER TODOS
- In `README.md` under `hifi test` section mention approximate time required for completion of command.

- `hifi test` - memory issue for hicanu when running on local lab system 

- Provide option for keeping all output files or only final output files after run is complete.
    `keep_all_files` (default: )

- Option to use two assemblers (most likely hifiasm-meta and metaflye) or all three assemblers
    
- Assembler option, hifiasm-meta --> read selection

- Options to provide in config.yaml
    - BiG-SCAPE
    - Antismash
    - Assemblers
    - Memory

- Test data: Add some unmapped reads to it

- BiG-SLICE: Search against BiG-SLICE dataset

- `hifibgc install` command --> Add option for putting database to a specified directory. However it's not only database, it also downloads a tool BiG-SCAPE and the command `python {input.BIGSCAPE_BIN_DIR}/BiG-SCAPE-1.1.5/bigscape.py` used in hifibgc.smk requires the path where this tool is put.
    Sizes of directories are:
        bigscape - 3.3G
        antismash - 8.5G
        Total ~ 12G

## LAST TODOS
- `hifibgc config` command --> See in hifi_bgc.md
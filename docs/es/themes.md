# Temas

Elige los colores del JSON desde el import. El tema predeterminado es `monokai`.
No necesitas un archivo de configuración. El tema aporta el fondo del bloque JSON;
no cambia el fondo de la terminal ni los colores HTTP o de assertions.
Las respuestas de texto y vacías no reciben resaltado JSON. Se omiten las secciones
vacías. Los bordes y separadores usan un color neutro suave.

Todas las pestañas muestran el **mismo response protegido**, exportado desde el
renderizador Rich de producción a 90 columnas. La fuente y los colores pueden
variar según tu terminal. `ansi_dark` y `ansi_light` usan la paleta de tu terminal;
estas muestras usan la misma paleta oscura para comparar. Usa `ansi_light` en una
terminal clara.

Los nombres disponibles dependen de tu versión instalada de Pygments. Un nombre
inválido muestra las opciones disponibles. Para consultarlas en tu entorno:

```bash
python -c "from request_logger.theme import available_themes; print(', '.join(available_themes()))"
```

## Vista previa de temas

=== "monokai"

    ### monokai

    ```robotframework
    *** Settings ***
    Library    RequestLogger    mode=full    syntax_theme=monokai
    ```

    ![monokai](assets/themes/monokai.svg)

=== "abap"

    ### abap

    ```robotframework
    *** Settings ***
    Library    RequestLogger    mode=full    syntax_theme=abap
    ```

    ![abap](assets/themes/abap.svg)

=== "algol"

    ### algol

    ```robotframework
    *** Settings ***
    Library    RequestLogger    mode=full    syntax_theme=algol
    ```

    ![algol](assets/themes/algol.svg)

=== "algol_nu"

    ### algol_nu

    ```robotframework
    *** Settings ***
    Library    RequestLogger    mode=full    syntax_theme=algol_nu
    ```

    ![algol_nu](assets/themes/algol_nu.svg)

=== "ansi_dark"

    ### ansi_dark

    ```robotframework
    *** Settings ***
    Library    RequestLogger    mode=full    syntax_theme=ansi_dark
    ```

    ![ansi_dark](assets/themes/ansi_dark.svg)

=== "ansi_light"

    ### ansi_light

    ```robotframework
    *** Settings ***
    Library    RequestLogger    mode=full    syntax_theme=ansi_light
    ```

    ![ansi_light](assets/themes/ansi_light.svg)

=== "arduino"

    ### arduino

    ```robotframework
    *** Settings ***
    Library    RequestLogger    mode=full    syntax_theme=arduino
    ```

    ![arduino](assets/themes/arduino.svg)

=== "autumn"

    ### autumn

    ```robotframework
    *** Settings ***
    Library    RequestLogger    mode=full    syntax_theme=autumn
    ```

    ![autumn](assets/themes/autumn.svg)

=== "borland"

    ### borland

    ```robotframework
    *** Settings ***
    Library    RequestLogger    mode=full    syntax_theme=borland
    ```

    ![borland](assets/themes/borland.svg)

=== "bw"

    ### bw

    ```robotframework
    *** Settings ***
    Library    RequestLogger    mode=full    syntax_theme=bw
    ```

    ![bw](assets/themes/bw.svg)

=== "coffee"

    ### coffee

    ```robotframework
    *** Settings ***
    Library    RequestLogger    mode=full    syntax_theme=coffee
    ```

    ![coffee](assets/themes/coffee.svg)

=== "colorful"

    ### colorful

    ```robotframework
    *** Settings ***
    Library    RequestLogger    mode=full    syntax_theme=colorful
    ```

    ![colorful](assets/themes/colorful.svg)

=== "default"

    ### default

    ```robotframework
    *** Settings ***
    Library    RequestLogger    mode=full    syntax_theme=default
    ```

    ![default](assets/themes/default.svg)

=== "dracula"

    ### dracula

    ```robotframework
    *** Settings ***
    Library    RequestLogger    mode=full    syntax_theme=dracula
    ```

    ![dracula](assets/themes/dracula.svg)

=== "emacs"

    ### emacs

    ```robotframework
    *** Settings ***
    Library    RequestLogger    mode=full    syntax_theme=emacs
    ```

    ![emacs](assets/themes/emacs.svg)

=== "friendly"

    ### friendly

    ```robotframework
    *** Settings ***
    Library    RequestLogger    mode=full    syntax_theme=friendly
    ```

    ![friendly](assets/themes/friendly.svg)

=== "friendly_grayscale"

    ### friendly_grayscale

    ```robotframework
    *** Settings ***
    Library    RequestLogger    mode=full    syntax_theme=friendly_grayscale
    ```

    ![friendly_grayscale](assets/themes/friendly_grayscale.svg)

=== "fruity"

    ### fruity

    ```robotframework
    *** Settings ***
    Library    RequestLogger    mode=full    syntax_theme=fruity
    ```

    ![fruity](assets/themes/fruity.svg)

=== "github-dark"

    ### github-dark

    ```robotframework
    *** Settings ***
    Library    RequestLogger    mode=full    syntax_theme=github-dark
    ```

    ![github-dark](assets/themes/github-dark.svg)

=== "gruvbox-dark"

    ### gruvbox-dark

    ```robotframework
    *** Settings ***
    Library    RequestLogger    mode=full    syntax_theme=gruvbox-dark
    ```

    ![gruvbox-dark](assets/themes/gruvbox-dark.svg)

=== "gruvbox-light"

    ### gruvbox-light

    ```robotframework
    *** Settings ***
    Library    RequestLogger    mode=full    syntax_theme=gruvbox-light
    ```

    ![gruvbox-light](assets/themes/gruvbox-light.svg)

=== "igor"

    ### igor

    ```robotframework
    *** Settings ***
    Library    RequestLogger    mode=full    syntax_theme=igor
    ```

    ![igor](assets/themes/igor.svg)

=== "inkpot"

    ### inkpot

    ```robotframework
    *** Settings ***
    Library    RequestLogger    mode=full    syntax_theme=inkpot
    ```

    ![inkpot](assets/themes/inkpot.svg)

=== "lightbulb"

    ### lightbulb

    ```robotframework
    *** Settings ***
    Library    RequestLogger    mode=full    syntax_theme=lightbulb
    ```

    ![lightbulb](assets/themes/lightbulb.svg)

=== "lilypond"

    ### lilypond

    ```robotframework
    *** Settings ***
    Library    RequestLogger    mode=full    syntax_theme=lilypond
    ```

    ![lilypond](assets/themes/lilypond.svg)

=== "lovelace"

    ### lovelace

    ```robotframework
    *** Settings ***
    Library    RequestLogger    mode=full    syntax_theme=lovelace
    ```

    ![lovelace](assets/themes/lovelace.svg)

=== "manni"

    ### manni

    ```robotframework
    *** Settings ***
    Library    RequestLogger    mode=full    syntax_theme=manni
    ```

    ![manni](assets/themes/manni.svg)

=== "material"

    ### material

    ```robotframework
    *** Settings ***
    Library    RequestLogger    mode=full    syntax_theme=material
    ```

    ![material](assets/themes/material.svg)

=== "murphy"

    ### murphy

    ```robotframework
    *** Settings ***
    Library    RequestLogger    mode=full    syntax_theme=murphy
    ```

    ![murphy](assets/themes/murphy.svg)

=== "native"

    ### native

    ```robotframework
    *** Settings ***
    Library    RequestLogger    mode=full    syntax_theme=native
    ```

    ![native](assets/themes/native.svg)

=== "night-owl"

    ### night-owl

    ```robotframework
    *** Settings ***
    Library    RequestLogger    mode=full    syntax_theme=night-owl
    ```

    ![night-owl](assets/themes/night-owl.svg)

=== "nord"

    ### nord

    ```robotframework
    *** Settings ***
    Library    RequestLogger    mode=full    syntax_theme=nord
    ```

    ![nord](assets/themes/nord.svg)

=== "nord-darker"

    ### nord-darker

    ```robotframework
    *** Settings ***
    Library    RequestLogger    mode=full    syntax_theme=nord-darker
    ```

    ![nord-darker](assets/themes/nord-darker.svg)

=== "one-dark"

    ### one-dark

    ```robotframework
    *** Settings ***
    Library    RequestLogger    mode=full    syntax_theme=one-dark
    ```

    ![one-dark](assets/themes/one-dark.svg)

=== "paraiso-dark"

    ### paraiso-dark

    ```robotframework
    *** Settings ***
    Library    RequestLogger    mode=full    syntax_theme=paraiso-dark
    ```

    ![paraiso-dark](assets/themes/paraiso-dark.svg)

=== "paraiso-light"

    ### paraiso-light

    ```robotframework
    *** Settings ***
    Library    RequestLogger    mode=full    syntax_theme=paraiso-light
    ```

    ![paraiso-light](assets/themes/paraiso-light.svg)

=== "pastie"

    ### pastie

    ```robotframework
    *** Settings ***
    Library    RequestLogger    mode=full    syntax_theme=pastie
    ```

    ![pastie](assets/themes/pastie.svg)

=== "perldoc"

    ### perldoc

    ```robotframework
    *** Settings ***
    Library    RequestLogger    mode=full    syntax_theme=perldoc
    ```

    ![perldoc](assets/themes/perldoc.svg)

=== "rainbow_dash"

    ### rainbow_dash

    ```robotframework
    *** Settings ***
    Library    RequestLogger    mode=full    syntax_theme=rainbow_dash
    ```

    ![rainbow_dash](assets/themes/rainbow_dash.svg)

=== "rrt"

    ### rrt

    ```robotframework
    *** Settings ***
    Library    RequestLogger    mode=full    syntax_theme=rrt
    ```

    ![rrt](assets/themes/rrt.svg)

=== "sas"

    ### sas

    ```robotframework
    *** Settings ***
    Library    RequestLogger    mode=full    syntax_theme=sas
    ```

    ![sas](assets/themes/sas.svg)

=== "solarized-dark"

    ### solarized-dark

    ```robotframework
    *** Settings ***
    Library    RequestLogger    mode=full    syntax_theme=solarized-dark
    ```

    ![solarized-dark](assets/themes/solarized-dark.svg)

=== "solarized-light"

    ### solarized-light

    ```robotframework
    *** Settings ***
    Library    RequestLogger    mode=full    syntax_theme=solarized-light
    ```

    ![solarized-light](assets/themes/solarized-light.svg)

=== "staroffice"

    ### staroffice

    ```robotframework
    *** Settings ***
    Library    RequestLogger    mode=full    syntax_theme=staroffice
    ```

    ![staroffice](assets/themes/staroffice.svg)

=== "stata-dark"

    ### stata-dark

    ```robotframework
    *** Settings ***
    Library    RequestLogger    mode=full    syntax_theme=stata-dark
    ```

    ![stata-dark](assets/themes/stata-dark.svg)

=== "stata-light"

    ### stata-light

    ```robotframework
    *** Settings ***
    Library    RequestLogger    mode=full    syntax_theme=stata-light
    ```

    ![stata-light](assets/themes/stata-light.svg)

=== "tango"

    ### tango

    ```robotframework
    *** Settings ***
    Library    RequestLogger    mode=full    syntax_theme=tango
    ```

    ![tango](assets/themes/tango.svg)

=== "trac"

    ### trac

    ```robotframework
    *** Settings ***
    Library    RequestLogger    mode=full    syntax_theme=trac
    ```

    ![trac](assets/themes/trac.svg)

=== "vim"

    ### vim

    ```robotframework
    *** Settings ***
    Library    RequestLogger    mode=full    syntax_theme=vim
    ```

    ![vim](assets/themes/vim.svg)

=== "vs"

    ### vs

    ```robotframework
    *** Settings ***
    Library    RequestLogger    mode=full    syntax_theme=vs
    ```

    ![vs](assets/themes/vs.svg)

=== "xcode"

    ### xcode

    ```robotframework
    *** Settings ***
    Library    RequestLogger    mode=full    syntax_theme=xcode
    ```

    ![xcode](assets/themes/xcode.svg)

=== "zenburn"

    ### zenburn

    ```robotframework
    *** Settings ***
    Library    RequestLogger    mode=full    syntax_theme=zenburn
    ```

    ![zenburn](assets/themes/zenburn.svg)


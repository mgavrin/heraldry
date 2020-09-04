Resources for generating SCA armory art.

Known issues: Sometimes for multiply striped fields (barry, chevronelly, etc) the tincture in the dexter chief corner is not the first one in the list passed in. Change the order of the list as a workaround.

TODO: type hints

* Field divisions
  * Supported:
    * Per pale
    * Per fess
    * Paly
    * Barry
    * Per bend
    * Per bend sinister
    * Bendy
    * Bendy sinister
    * Per chevron
    * Chevronelly
    * Per chevron inverted
    * Chevronelly inverted
    * Per chevron throughout
    * Per chevron inverted througout
    * Quarterly
    * In canton
    * Per saltire
    * Vetu
    * Vetu ploye
  * TODO:
    * Per pall
    * Per pall reversed
    * Gyronny 8
    * Gyronny 10
    * Checky
    * Lozengy
    * Fretty
    * Scaly
    * Masoned

* Complex lines of division
  * Assemble sets of points/curves for complex lines
  * Treat a complex line of division as a rectangle with the line through it; colorswap and rotate as necessary
  * Supported:
  * TODO:
    * Indented
    * Rayonny
    * Embattled
      * counter-embattled
      * embattled-counter-embattled
      * bretesse
      * dovetailed
    * Wavy
    * Nebuly
    * Engrailed (points go out/down/sinister)
    * Invected (points go in/up/dexter))
    * Dancetty
    * Enarched/Ploye
    * Flory-counterflory
    * Indented fleury at the points
    * Lozengy
    * Potenty
    * Raguly
    * Urdy
    * Enarched
    * Bevilled ([per] bend [sinister] only)
    * Denticulada (bordures only)
    * Right step/left step (per fess only)
    * Rompu (chevron only)
    * Triangular (chief only)
    * Engouled (bend [sinister] only)

* Ordinaries
  * Pale
  * Pallet
  * Fess
  * Bar
  * Bend
  * Bend sinister
  * Bendlet
  * Chief
    * Also support as "label"
  * Chevron
  * Chevronel
  * Mount
  * Pall
  * Pall reversed
  * Bordure
  * Base
  * Point pointed
  * Quarter
  * Canton
  * Gyron
  * Orle
  * Double tressure
  * Tierce
  * Flaunches
  * Cotised
  * Endorsed  

* Geometric charges
  * Roundel
    * Bezant
    * Torteau
  * Billet
  * Crescent
  * Increscent
  * Decrescent
  * Crescent pendant
  * Fleur-de-lys
  * Lozenge
  * Mascle
  * Masculyn
  * Pheon
  * Delf

* Lion postures
  * Affronty
  * Sejant affronty
  * Sejant erect affronty
  * Contourny versions of all the below
  * Rampant
  * Salient
  * Sejant
  * Sejant erect
  * Guardant
  * Couchant
  * Passant
  * Courant
  * Statant
  * Dormant
  
* Bonus winged lion postures
  * Segreant
  * Segreant contourny

* Bird postures
  * Displayed
  * Contourny versions of all the below
  * Volant
  * Close
  * Naiant
  * Rising
  * Striking
  * Roussant
  * Volant wings addorsed
  
* Fish postures
  * Haurient
  * Urinant
  * Naiant
  * Naiant contourny

* Arrangements of e.g. mullets
  * In pale
  * In fess
  * In bend
  * In bend sinister
  * In chief
  * In base
  * Maintaining
  * Sustaining
  * Surmounted
  * Overall

* Other stuff
  * Voided
  * Fimbriated

* UI
  * tkinter file picker for charges
  * color picker
    * recolor everything that isn't black (outlines)
    * if the selected color is sable, swap black to white
  * drag and drop to move charges around the field
  * resize charges with corner arrows

* Acquire art assets
  * Lion (for quadruped postures)
  * Bird (for bird postures)
  * Crescent
  * Mullet
  * Pheon
  * Estoile
  * Ermine
  * Vair
  * Figure out how to go through an image pixel by pixel and swap colors,
    so you can have arbitrary tinctures of ermine and vair and arbitrary tinctures around a complex line
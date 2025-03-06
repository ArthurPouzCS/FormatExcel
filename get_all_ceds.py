import re


text = """
    DÉCHETS PROVENANT DE L'EXPLORATION ET DE L'EXPLOITATION DES MINES ET DES CARRIÈRES AINSI QUE DU TRAITEMENT PHYSIQUE ET CHIMIQUE
    DES MINÉRAUX
    01 01 déchets provenant de l'extraction des minéraux
    01 01 01 déchets provenant de l'extraction des minéraux métallifères
    01 01 02 déchets provenant de l'extraction des minéraux non métallifères
    01 03 déchets provenant de la transformation physique et chimique des minéraux métallifères
    01 03 04* stériles acidogènes provenant de la transformation du sulfure
    01 03 05* autres stériles contenant des substances dangereuses
    01 03 06 stériles autres que ceux visés aux rubriques 01 03 04 et 01 03 05
    01 03 07* autres déchets contenant des substances dangereuses provenant de la transformation physique et chimique des minéraux métallifères
    01 03 08 déchets de poussières et de poudres autres que ceux visés à la rubrique 01 03 07
    01 03 09 boues rouges issues de la production d'alumine autres que celles visées à la rubrique 01 03 10
    01 03 10* boues rouges issues de la production d'alumine contenant des substances dangereuses, autres que les déchets visés à la rubrique 01 03 07
    01 03 99 déchets non spécifiés ailleurs
    01 04 déchets provenant de la transformation physique et chimique des minéraux non métallifères
    01 04 07* déchets contenant des substances dangereuses provenant de la transformation physique et chimique des minéraux non métallifères
    01 04 08 déchets de graviers et débris de pierres autres que ceux visés à la rubrique 01 04 07
    01 04 09 déchets de sable et d'argile
    01 04 10 déchets de poussières et de poudres autres que ceux visés à la rubrique 01 04 07
    01 04 11 déchets de la transformation de la potasse et des sels minéraux autres que ceux visés à la rubrique 01 04 07
    01 04 12 stériles et autres déchets provenant du lavage et du nettoyage des minéraux autres que ceux visés aux rubriques 01 04 07 et 01 04 11
    01 04 13 déchets provenant de la taille et du sciage des pierres autres que ceux visés à la rubrique 01 04 07
    01 04 99 déchets non spécifiés ailleurs
    01 05 boues de forage et autres déchets de forage
    01 05 04 boues et autres déchets de forage à l'eau douce
    01 05 05* boues et autres déchets de forage contenant des hydrocarbures
    01 05 06* boues de forage et autres déchets de forage contenant des substances dangereuses
    01 05 07 boues et autres déchets de forage contenant des sels de baryum, autres que ceux visés aux rubriques 01 05 05 et 01 05 06
    01 05 08 boues et autres déchets de forage contenant des chlorures, autres que ceux visés aux rubriques 01 05 05 et 01 05 06
    01 05 99 déchets non spécifiés ailleurs
    2
    DÉCHETS PROVENANT DE L'AGRICULTURE, DE L'HORTICULTURE, DE L'AQUACULTURE, DE LA SYLVICULTURE, DE LA CHASSE ET DE LA PÊCHE AINSI QUE
    DE LA PRÉPARATION ET DE LA TRANSFORMATION DES ALIMENTS
    02 01 déchets provenant de l'agriculture, de l'horticulture, de l'aquaculture, de la sylviculture, de la chasse et de la pêche
    02 01 01 boues provenant du lavage et du nettoyage
    02 01 02 déchets de tissus animaux
    02 01 03 déchets de tissus végétaux
    02 01 04 déchets de matières plastiques (à l'exclusion des emballages)
    02 01 06 fèces, urine et fumier (y compris paille souillée), effluents, collectés séparément et traités hors site
    02 01 07 déchets provenant de la sylviculture
    02 01 08* déchets agrochimiques contenant des substances dangereuses
    02 01 09 déchets agrochimiques autres que ceux visés à la rubrique 02 01 08
    02 01 10 déchets métalliques
    02 01 99 déchets non spécifiés ailleurs
    02 02 déchets provenant de la préparation et de la transformation de la viande, des poissons et autres aliments d'origine animale
    02 02 01 boues provenant du lavage et du nettoyage
    02 02 02 déchets de tissus animaux
    02 02 03 matières impropres à la consommation ou à la transformation
    02 02 04 boues provenant du traitement in situ des effluents
    02 02 99 déchets non spécifiés ailleurs
    02 03 déchets provenant de la préparation et de la transformation des fruits, des légumes, des céréales, des huiles alimentaires, du cacao, du café, du thé
    et du tabac, de la production de conserves, de la production de levures et d'extraits de levures, de la préparation et de la fermentation de mélasses
    02 03 01 boues provenant du lavage, du nettoyage, de l'épluchage, de la centrifugation et de la séparation
    02 03 02 déchets d'agents de conservation
    02 03 03 déchets de l'extraction aux solvants
    02 03 04 matières impropres à la consommation ou à la transformation
    02 03 05 boues provenant du traitement in situ des effluents
    02 03 99 déchets non spécifiés ailleurs
    02 04 déchets de la transformation du sucre
    02 04 01 terre provenant du lavage et du nettoyage des betteraves
    02 04 02 carbonate de calcium déclassé
    02 04 03 boues provenant du traitement in situ des effluents
    02 04 99 déchets non spécifiés ailleurs
    02 05 déchets provenant de l'industrie des produits laitiers
    02 05 01 matières impropres à la consommation ou à la transformation
    02 05 02 boues provenant du traitement in situ des effluents
    02 05 99 déchets non spécifiés ailleurs
    02 06 déchets de boulangerie, pâtisserie, confiserie
    02 06 01 matières impropres à la consommation ou à la transformation
    02 06 02 déchets d'agents de conservation
    02 06 03 boues provenant du traitement in situ des effluents
    02 06 99 déchets non spécifiés ailleurs
    02 07 déchets provenant de la production de boissons alcooliques et non alcooliques (sauf café, thé et cacao)
    02 07 01 déchets provenant du lavage, du nettoyage et de la réduction mécanique des matières premières
    02 07 02 déchets de la distillation de l'alcool
    02 07 03 déchets de traitements chimiques
    02 07 04 matières impropres à la consommation ou à la transformation
    02 07 05 boues provenant du traitement in situ des effluents
    02 07 99 déchets non spécifiés ailleurs
    3
    DÉCHETS PROVENANT DE LA TRANSFORMATION DU BOIS ET DE LA PRODUCTION DE PANNEAUX ET DE MEUBLES, DE PÂTE À PAPIER, DE PAPIER ET DE
    CARTON
    03 01 déchets provenant de la transformation du bois et de la fabrication de panneaux et de meubles
    03 01 01 déchets d'écorce et de liège
    03 01 04* sciure de bois, copeaux, chutes, bois, panneaux de particules et placages contenant des substances dangereuses
    03 01 05 sciure de bois, copeaux, chutes, bois, panneaux de particules et placages autres que ceux visés à la rubrique 03 01 04
    03 01 99 déchets non spécifiés ailleurs
    03 02 déchets des produits de protection du bois
    03 02 01* composés organiques non halogénés de protection du bois
    03 02 02* composés organochlorés de protection du bois
    03 02 03* composés organométalliques de protection du bois
    03 02 04* composés inorganiques de protection du bois
    03 02 05* autres produits de protection du bois contenant des substances dangereuses
    03 02 99 produits de protection du bois non spécifiés ailleurs
    03 03 déchets provenant de la production et de la transformation de papier, de carton et de pâte à papier
    03 03 01 déchets d'écorce et de bois
    03 03 02 liqueurs vertes (provenant de la récupération de liqueur de cuisson)
    03 03 05 boues de désencrage provenant du recyclage du papier
    03 03 07 refus séparés mécaniquement provenant du broyage de déchets de papier et de carton
    03 03 08 déchets provenant du tri de papier et de carton destinés au recyclage
    03 03 09 déchets de boues résiduaires de chaux
    03 03 10 refus fibreux, boues de fibres, de charge et de couchage provenant d'une séparation mécanique
    03 03 11 boues provenant du traitement in situ des effluents autres que celles visées à la rubrique 03 03 10
    03 03 99 déchets non spécifiés ailleurs
    4 DÉCHETS PROVENANT DES INDUSTRIES DU CUIR, DE LA FOURRURE ET DU TEXTILE
    04 01 déchets provenant de l'industrie du cuir et de la fourrure
    04 01 01 déchets d'écharnage et refentes
    04 01 02 résidus de pelanage
    04 01 03* déchets de dégraissage contenant des solvants sans phase liquide
    04 01 04 liqueur de tannage contenant du chrome
    04 01 05 liqueur de tannage sans chrome
    04 01 06 boues, notamment provenant du traitement in situ des effluents, contenant du chrome
    04 01 07 boues, notamment provenant du traitement in situ des effluents, sans chrome
    04 01 08 déchets de cuir tanné (refentes sur bleu, dérayures, échantillonnages, poussières de ponçage), contenant du chrome
    04 01 09 déchets provenant de l'habillage et des finitions
    04 01 99 déchets non spécifiés ailleurs
    04 02 déchets de l'industrie textile
    04 02 09 matériaux composites (textile imprégné, élastomère, plastomère)
    04 02 10 matières organiques issues de produits naturels (par exemple graisse, cire)
    04 02 14* déchets provenant des finitions contenant des solvants organiques
    04 02 15 déchets provenant des finitions autres que ceux visés à la rubrique 04 02 14
    04 02 16* teintures et pigments contenant des substances dangereuses
    04 02 17 teintures et pigments autres que ceux visés à la rubrique 04 02 16
    04 02 19* boues provenant du traitement in situ des effluents contenant des substances dangereuses
    04 02 20 boues provenant du traitement in situ des effluents autres que celles visées à la rubrique 04 02 19
    04 02 21 fibres textiles non ouvrées
    04 02 22 fibres textiles ouvrées
    04 02 99 déchets non spécifiés ailleurs
    5 DÉCHETS PROVENANT DU RAFFINAGE DU PÉTROLE, DE LA PURIFICATION DU GAZ NATUREL ET DU TRAITEMENT PYROLYTIQUE DU CHARBON
    05 01 déchets provenant du raffinage du pétrole
    05 01 02* boues de dessalage
    05 01 03* boues de fond de cuves
    05 01 04* boues d'alkyles acides
    05 01 05* hydrocarbures accidentellement répandus
    05 01 06* boues contenant des hydrocarbures provenant des opérations de maintenance de l'installation ou des équipements
    05 01 07* goudrons acides
    05 01 08* autres goudrons
    05 01 09* boues provenant du traitement in situ des effluents contenant des substances dangereuses
    05 01 10 boues provenant du traitement in situ des effluents autres que celles visées à la rubrique 05 01 09
    05 01 11* déchets provenant du nettoyage d'hydrocarbures avec des bases
    05 01 12* hydrocarbures contenant des acides
    05 01 13 boues du traitement de l'eau d'alimentation des chaudières
    05 01 14 déchets provenant des colonnes de refroidissement
    05 01 15* argiles de filtration usées
    05 01 16 déchets contenant du soufre provenant de la désulfuration du pétrole
    05 01 17 mélanges bitumineux
    05 01 99 déchets non spécifiés ailleurs
    05 06 déchets provenant du traitement pyrolytique du charbon
    05 06 01* goudrons acides
    05 06 03* autres goudrons
    05 06 04 déchets provenant des colonnes de refroidissement
    05 06 99 déchets non spécifiés ailleurs
    05 07 déchets provenant de la purification et du transport du gaz naturel
    05 07 01* déchets contenant du mercure
    05 07 02 déchets contenant du soufre
    05 07 99 déchets non spécifiés ailleurs
    6 DÉCHETS DES PROCÉDÉS DE LA CHIMIE MINÉRALE
    06 01 déchets provenant de la fabrication, formulation, distribution et utilisation (FFDU) d'acides
    06 01 01* acide sulfurique et acide sulfureux
    06 01 02* acide chlorhydrique
    06 01 03* acide fluorhydrique
    06 01 04* acide phosphorique et acide phosphoreux
    06 01 05* acide nitrique et acide nitreux
    06 01 06* autres acides
    06 01 99 déchets non spécifiés ailleurs
    06 02 déchets provenant de la FFDU de bases
    06 02 01* hydroxyde de calcium
    06 02 03* hydroxyde d'ammonium
    06 02 04* hydroxyde de sodium et hydroxyde de potassium
    06 02 05* autres bases
    06 02 99 déchets non spécifiés ailleurs
    06 03 déchets provenant de la FFDU de sels et leurs solutions et d'oxydes métalliques
    06 03 11* sels et solutions contenant des cyanures
    06 03 13* sels et solutions contenant des métaux lourds
    06 03 14 sels solides et solutions autres que ceux visés aux rubriques 06 03 11 et 06 03 13
    06 03 15* oxydes métalliques contenant des métaux lourds
    06 03 16 oxydes métalliques autres que ceux visés à la rubrique 06 03 15
    06 03 99 déchets non spécifiés ailleurs
    06 04 déchets contenant des métaux autres que ceux visés à la section 06 03
    06 04 03* déchets contenant de l'arsenic
    06 04 04* déchets contenant du mercure
    06 04 05* déchets contenant d'autres métaux lourds
    06 04 99 déchets non spécifiés ailleurs
    06 05 boues provenant du traitement in situ des effluents
    06 05 02* boues provenant du traitement in situ des effluents contenant des substances dangereuses
    06 05 03 boues provenant du traitement in situ des effluents autres que celles visées à la rubrique 06 05 02
    06 06 déchets provenant de la FFDU de produits chimiques contenant du soufre, de la chimie du soufre et des procédés de désulfuration
    06 06 02* déchets contenant des sulfures dangereux
    06 06 03 déchets contenant des sulfures autres que ceux visés à la rubrique 06 06 02
    06 06 99 déchets non spécifiés ailleurs
    06 07 déchets provenant de la FFDU des halogènes et de la chimie des halogènes
    06 07 01* déchets contenant de l'amiante provenant de l'électrolyse
    06 07 02* déchets de charbon actif utilisé pour la production du chlore
    06 07 03* boues de sulfate de baryum contenant du mercure
    06 07 04* solutions et acides, par exemple acide de contact
    06 07 99 déchets non spécifiés ailleurs
    06 08 déchets provenant de la FFDU du silicium et des dérivés du silicium
    06 08 02* déchets contenant des chlorosilanes dangereux
    06 08 99 déchets non spécifiés ailleurs
    06 09 déchets provenant de la FFDU des produits chimiques contenant du phosphore et de la chimie du phosphore
    06 09 02 scories phosphoriques
    06 09 03* déchets de réactions basées sur le calcium contenant des substances dangereuses ou contaminées par de telles substances
    06 09 04 déchets de réactions basées sur le calcium autres que ceux visés à la rubrique 06 09 03
    06 09 99 déchets non spécifiés ailleurs
    06 10 déchets provenant de la FFDU de produits chimiques contenant de l'azote, de la chimie de l'azote et de la production d'engrais
    06 10 02* déchets contenant des substances dangereuses
    06 10 99 déchets non spécifiés ailleurs
    06 11 déchets provenant de la fabrication des pigments inorganiques et des opacifiants
    06 11 01 déchets de réactions basées sur le calcium provenant de la production de dioxyde de titane
    06 11 99 déchets non spécifiés ailleurs
    06 13 déchets des procédés de la chimie minérale non spécifiés ailleurs
    06 13 01* produits phytosanitaires inorganiques, agents de protection du bois et autres biocides
    06 13 02* charbon actif usé (sauf rubrique 06 07 02)
    06 13 03 noir de carbone
    06 13 04* déchets provenant de la transformation de l'amiante
    06 13 05* suies
    06 13 99 déchets non spécifiés ailleurs
    7 DÉCHETS DES PROCÉDÉS DE LA CHIMIE ORGANIQUE
    07 01 déchets provenant de la fabrication, formulation, distribution et utilisation (FFDU) de produits organiques de base
    07 01 01* eaux de lavage et liqueurs mères aqueuses
    07 01 03* solvants, liquides de lavage et liqueurs mères organiques halogénés
    07 01 04* autres solvants, liquides de lavage et liqueurs mères organiques
    07 01 07* résidus de réaction et résidus de distillation halogénés
    07 01 08* autres résidus de réaction et résidus de distillation
    07 01 09* gâteaux de filtration et absorbants usés halogénés
    07 01 10* autres gâteaux de filtration et absorbants usés
    07 01 11* boues provenant du traitement in situ des effluents contenant des substances dangereuses
    07 01 12 boues provenant du traitement in situ des effluents autres que celles visées à la rubrique 07 01 11
    07 01 99 déchets non spécifiés ailleurs
    07 02 déchets provenant de la FFDU de matières plastiques, caoutchouc et fibres synthétiques
    07 02 01* eaux de lavage et liqueurs mères aqueuses
    07 02 03* solvants, liquides de lavage et liqueurs mères organiques halogénés
    07 02 04* autres solvants, liquides de lavage et liqueurs mères organiques
    07 02 07* résidus de réaction et résidus de distillation halogénés
    07 02 08* autres résidus de réaction et résidus de distillation
    07 02 09* gâteaux de filtration et absorbants usés halogénés
    07 02 10* autres gâteaux de filtration et absorbants usés
    07 02 11* boues provenant du traitement in situ des effluents contenant des substances dangereuses
    07 02 12 boues provenant du traitement in situ des effluents autres que celles visées à la rubrique 07 02 11
    07 02 13 déchets plastiques
    07 02 14* déchets provenant d'additifs contenant des substances dangereuses
    07 02 15 déchets provenant d'additifs autres que ceux visés à la rubrique 07 02 14
    07 02 16* déchets contenant des silicones dangereux
    07 02 17 déchets contenant des silicones autres que ceux visés à la rubrique 07 02 16
    07 02 99 déchets non spécifiés ailleurs
    07 03 déchets provenant de la FFDU de teintures et pigments organiques (sauf section 06 11)
    07 03 01* eaux de lavage et liqueurs mères aqueuses
    07 03 03* solvants, liquides de lavage et liqueurs mères organiques halogénés
    07 03 04* autres solvants, liquides de lavage et liqueurs mères organiques
    07 03 07* résidus de réaction et résidus de distillation halogénés
    07 03 08* autres résidus de réaction et résidus de distillation
    07 03 09* gâteaux de filtration et absorbants usés halogénés
    07 03 10* autres gâteaux de filtration et absorbants usés
    07 03 11* boues provenant du traitement in situ des effluents contenant des substances dangereuses
    07 03 12 boues provenant du traitement in situ des effluents autres que celles visées à la rubrique 07 03 11
    07 03 99 déchets non spécifiés ailleurs
    07 04 déchets provenant de la FFDU de produits phytosanitaires organiques (sauf rubriques 02 01 08 et 02 01 09), d'agents de protection du bois (sauf
    section 03 02) et d'autres biocides
    07 04 01* eaux de lavage et liqueurs mères aqueuses
    07 04 03* solvants, liquides de lavage et liqueurs mères organiques halogénés
    07 04 04* autres solvants, liquides de lavage et liqueurs mères organiques
    07 04 07* résidus de réaction et résidus de distillation halogénés
    07 04 08* autres résidus de réaction et résidus de distillation
    07 04 09* gâteaux de filtration et absorbants usés halogénés
    07 04 10* autres gâteaux de filtration et absorbants usés
    07 04 11* boues provenant du traitement in situ des effluents contenant des substances dangereuses
    07 04 12 boues provenant du traitement in situ des effluents autres que celles visées à la rubrique 07 04 11
    07 04 13* déchets solides contenant des substances dangereuses
    07 04 99 déchets non spécifiés ailleurs
    07 05 déchets provenant de la FFDU des produits pharmaceutiques
    07 05 01* eaux de lavage et liqueurs mères aqueuses
    07 05 03* solvants, liquides de lavage et liqueurs mères organiques halogénés
    07 05 04* autres solvants, liquides de lavage et liqueurs mères organiques
    07 05 07* résidus de réaction et résidus de distillation halogénés
    07 05 08* autres résidus de réaction et résidus de distillation
    07 05 09* gâteaux de filtration et absorbants usés halogénés
    07 05 10* autres gâteaux de filtration et absorbants usés
    07 05 11* boues provenant du traitement in situ des effluents contenant des substances dangereuses
    07 05 12 boues provenant du traitement in situ des effluents autres que celles visées à la rubrique 07 05 11
    07 05 13* déchets solides contenant des substances dangereuses
    07 05 14 déchets solides autres que ceux visés à la rubrique 07 05 13
    07 05 99 déchets non spécifiés ailleurs
    07 06 déchets provenant de la FFDU des corps gras, savons, détergents, désinfectants et cosmétiques
    07 06 01* eaux de lavage et liqueurs mères aqueuses
    07 06 03* solvants, liquides de lavage et liqueurs mères organiques halogénés
    07 06 04* autres solvants, liquides de lavage et liqueurs mères organiques
    07 06 07* résidus de réaction et résidus de distillation halogénés
    07 06 08* autres résidus de réaction et résidus de distillation
    07 06 09* gâteaux de filtration et absorbants usés halogénés
    07 06 10* autres gâteaux de filtration et absorbants usés
    07 06 11* boues provenant du traitement in situ des effluents contenant des substances dangereuses
    07 06 12 boues provenant du traitement in situ des effluents autres que celles visées à la rubrique 07 06 11
    07 06 99 déchets non spécifiés ailleurs
    07 07 déchets provenant de la FFDU de produits chimiques issus de la chimie fine et de produits chimiques non spécifiés ailleurs
    07 07 01* eaux de lavage et liqueurs mères aqueuses
    07 07 03* solvants, liquides de lavage et liqueurs mères organiques halogénés
    07 07 04* autres solvants, liquides de lavage et liqueurs mères organiques
    07 07 07* résidus de réaction et résidus de distillation halogénés
    07 07 08* autres résidus de réaction et résidus de distillation
    07 07 09* gâteaux de filtration et absorbants usés halogénés
    07 07 10* autres gâteaux de filtration et absorbants usés
    07 07 11* boues provenant du traitement in situ des effluents contenant des substances dangereuses
    07 07 12 boues provenant du traitement in situ des effluents autres que celles visées à la rubrique 07 07 11
    07 07 99 déchets non spécifiés ailleurs
    8
    DÉCHETS PROVENANT DE LA FABRICATION, DE LA FORMULATION, DE LA DISTRIBUTION ET DE L'UTILISATION (FFDU) DE PRODUITS DE REVÊTEMENT
    (PEINTURES, VERNIS ET ÉMAUX VITRIFIÉS), MASTICS ET ENCRES D'IMPRESSION
    08 01 déchets provenant de la FFDU et du décapage de peintures et vernis
    08 01 11* déchets de peintures et vernis contenant des solvants organiques ou d'autres substances dangereuses
    08 01 12 déchets de peintures ou vernis autres que ceux visés à la rubrique 08 01 11
    08 01 13* boues provenant de peintures ou vernis contenant des solvants organiques ou autres substances dangereuses
    08 01 14 boues provenant de peintures ou vernis autres que celles visées à la rubrique 08 01 13
    08 01 15* boues aqueuses contenant de la peinture ou du vernis contenant des solvants organiques ou autres substances dangereuses
    08 01 16 boues aqueuses contenant de la peinture ou du vernis autres que celles visées à la rubrique 08 01 15
    08 01 17* déchets provenant du décapage de peintures ou vernis contenant des solvants organiques ou autres substances dangereuses
    08 01 18 déchets provenant du décapage de peintures ou vernis autres que ceux visés à la rubrique 08 01 17
    08 01 19* boues aqueuses contenant de la peinture ou du vernis contenant des solvants organiques ou autres substances dangereuses
    08 01 20 suspensions aqueuses contenant de la peinture ou du vernis autres que celles visées à la rubrique 08 01 19
    08 01 21* déchets de décapants de peintures ou vernis
    08 01 99 déchets non spécifiés ailleurs
    08 02 déchets provenant de la FFDU d'autres produits de revêtement (y compris des matériaux céramiques)
    08 02 01 déchets de produits de revêtement en poudre
    08 02 02 boues aqueuses contenant des matériaux céramiques
    08 02 03 suspensions aqueuses contenant des matériaux céramiques
    08 02 99 déchets non spécifiés ailleurs
    08 03 déchets provenant de la FFDU d'encres d'impression
    08 03 07 boues aqueuses contenant de l'encre
    08 03 08 déchets liquides aqueux contenant de l'encre
    08 03 12* déchets d'encres contenant des substances dangereuses
    08 03 13 déchets d'encres autres que ceux visés à la rubrique 08 03 12
    08 03 14* boues d'encre contenant des substances dangereuses
    08 03 15 boues d'encre autres que celles visées à la rubrique 08 03 14
    08 03 16* déchets de solution de morsure
    08 03 17* déchets de toner d'impression contenant des substances dangereuses
    08 03 18 déchets de toner d'impression autres que ceux visés à la rubrique 08 03 17
    08 03 19* huiles dispersées
    08 03 99 déchets non spécifiés ailleurs
    08 04 déchets provenant de la FFDU de colles et mastics (y compris produits d'étanchéité)
    08 04 09* déchets de colles et mastics contenant des solvants organiques ou d'autres substances dangereuses
    08 04 10 déchets de colles et mastics autres que ceux visés à la rubrique 08 04 09
    08 04 11* boues de colles et mastics contenant des solvants organiques ou d'autres substances dangereuses
    08 04 12 boues de colles et mastics autres que celles visées à la rubrique 08 04 11
    08 04 13* boues aqueuses contenant des colles ou mastics contenant des solvants organiques ou d'autres substances dangereuses
    08 04 14 boues aqueuses contenant des colles et mastics autres que celles visées à la rubrique 08 04 13
    08 04 15* déchets liquides aqueux contenant des colles ou mastics contenant des solvants organiques ou d'autres substances dangereuses
    08 04 16 déchets liquides aqueux contenant des colles ou mastics autres que ceux visés à la rubrique 08 04 15
    08 04 17* huile de résine
    08 04 99 déchets non spécifiés ailleurs
    08 05 déchets non spécifiés ailleurs dans le chapitre 08
    08 05 01* déchets d'isocyanates
    9 DÉCHETS PROVENANT DE L'INDUSTRIE PHOTOGRAPHIQUE
    09 01 déchets de l'industrie photographique
    09 01 01* bains de développement aqueux contenant un activateur
    09 01 02* bains de développement aqueux pour plaques offset
    09 01 03* bains de développement contenant des solvants
    09 01 04* bains de fixation
    09 01 05* bains de blanchiment et bains de blanchiment/fixation
    09 01 06* déchets contenant de l'argent provenant du traitement in situ des déchets photographiques
    09 01 07 pellicules et papiers photographiques contenant de l'argent ou des composés de l'argent
    09 01 08 pellicules et papiers photographiques sans argent ni composés de l'argent
    09 01 10 appareils photographiques à usage unique sans piles
    09 01 11* appareils photographiques à usage unique contenant des piles visées aux rubriques 16 06 01, 16 06 02 ou 16 06 03
    09 01 12 appareils photographiques à usage unique contenant des piles autres que ceux visés à la rubrique 09 01 11
    09 01 13* déchets liquides aqueux provenant de la récupération in situ de l'argent autres que ceux visés à la rubrique 09 01 06
    09 01 99 déchets non spécifiés ailleurs
    10 DÉCHETS PROVENANT DE PROCÉDÉS THERMIQUES
    10 01 déchets provenant de centrales électriques et autres installations de combustion (sauf chapitre 19)
    10 01 01 mâchefers, scories et cendres sous chaudière (sauf cendres sous chaudière visées à la rubrique 10 01 04)
    10 01 02 cendres volantes de charbon
    10 01 03 cendres volantes de tourbe et de bois non traité
    10 01 04* cendres volantes et cendres sous chaudière d'hydrocarbures
    10 01 05 déchets solides de réactions basées sur le calcium, provenant de la désulfuration des gaz de fumée
    10 01 07 boues de réactions basées sur le calcium, provenant de la désulfuration des gaz de fumée
    10 01 09* acide sulfurique
    10 01 13* cendres volantes provenant d'hydrocarbures émulsifiés employés comme combustibles
    10 01 14* mâchefers, scories et cendres sous chaudière provenant de la coïncinération contenant des substances dangereuses
    10 01 15 mâchefers, scories et cendres sous chaudière provenant de la coïncinération autres que ceux visés à la rubrique 10 01 14
    10 01 16* cendres volantes provenant de la coïncinération contenant des substances dangereuses
    10 01 17 cendres volantes provenant de la coïncinération autres que celles visées à la rubrique 10 01 16
    10 01 18* déchets provenant de l'épuration des gaz contenant des substances dangereuses
    10 01 19 déchets provenant de l'épuration des gaz autres que ceux visés aux rubriques 10 01 05, 10 01 07 et 10 01 18
    10 01 20* boues provenant du traitement in situ des effluents contenant des substances dangereuses
    10 01 21 boues provenant du traitement in situ des effluents autres que celles visées à la rubrique 10 01 20
    10 01 22* boues aqueuses provenant du nettoyage des chaudières contenant des substances dangereuses
    10 01 23 boues aqueuses provenant du nettoyage des chaudières autres que celles visées à la rubrique 10 01 22
    10 01 24 sables provenant de lits fluidisés
    10 01 25 déchets provenant du stockage et de la préparation des combustibles des centrales à charbon
    10 01 26 déchets provenant de l'épuration des eaux de refroidissement
    10 01 99 déchets non spécifiés ailleurs
    10 02 déchets provenant de l'industrie du fer et de l'acier
    10 02 01 déchets de laitiers de hauts fourneaux et d'aciéries
    10 02 02 laitiers non traités
    10 02 07* déchets solides provenant de l'épuration des fumées contenant des substances dangereuses
    10 02 08 déchets solides provenant de l'épuration des fumées autres que ceux visés à la rubrique 10 02 07
    10 02 10 battitures de laminoir
    10 02 11* déchets provenant de l'épuration des eaux de refroidissement contenant des hydrocarbures
    10 02 12 déchets provenant de l'épuration des eaux de refroidissement autres que ceux visés à la rubrique 10 02 11
    10 02 13* boues et gâteaux de filtration provenant de l'épuration des fumées contenant des substances dangereuses
    10 02 14 boues et gâteaux de filtration provenant de l'épuration des fumées autres que ceux visés à la rubrique 10 02 13
    10 02 15 autres boues et gâteaux de filtration
    10 02 99 déchets non spécifiés ailleurs
    10 03 déchets de la pyrométallurgie de l'aluminium
    10 03 02 déchets d'anodes
    10 03 04* scories provenant de la production primaire
    10 03 05 déchets d'alumine
    10 03 08* scories salées de seconde fusion
    10 03 09* crasses noires de seconde fusion
    10 03 15* écumes inflammables ou émettant, au contact de l'eau, des gaz inflammables en quantités dangereuses
    10 03 16 écumes autres que celles visées à la rubrique 10 03 15
    10 03 17* déchets goudronnés provenant de la fabrication des anodes
    10 03 18 déchets carbonés provenant de la fabrication des anodes autres que ceux visés à la rubrique 10 03 17
    10 03 19* poussières de filtration des fumées contenant des substances dangereuses
    10 03 20 poussières de filtration des fumées autres que celles visées à la rubrique 10 03 19
    10 03 21* autres fines et poussières (y compris fines de broyage de crasses) contenant des substances dangereuses
    10 03 22 autres fines et poussières (y compris fines de broyage de crasses) autres que celles visées à la rubrique 10 03 21
    10 03 23* déchets solides provenant de l'épuration des fumées contenant des substances dangereuses
    10 03 24 déchets solides provenant de l'épuration des fumées autres que ceux visés à la rubrique 10 03 23
    10 03 25* boues et gâteaux de filtration provenant de l'épuration des fumées contenant des substances dangereuses
    10 03 26 boues et gâteaux de filtration provenant de l'épuration des fumées autres que ceux visés à la rubrique 10 03 25
    10 03 27* déchets provenant de l'épuration des eaux de refroidissement contenant des hydrocarbures
    10 03 28 déchets provenant de l'épuration des eaux de refroidissement autres que ceux visés à la rubrique 10 03 27
    10 03 29* déchets provenant du traitement des scories salées et du traitement des crasses noires contenant des substances dangereuses
    10 03 30 déchets provenant du traitement des scories salées et du traitement des crasses noires autres que ceux visés à la rubrique 10 03 29
    10 03 99 déchets non spécifiés ailleurs
    10 04 déchets provenant de la pyrométallurgie du plomb
    10 04 01* scories provenant de la production primaire et secondaire
    10 04 02* crasses et écumes provenant de la production primaire et secondaire
    10 04 03* arséniate de calcium
    10 04 04* poussières de filtration des fumées
    10 04 05* autres fines et poussières
    10 04 06* déchets solides provenant de l'épuration des fumées
    10 04 07* boues et gâteaux de filtration provenant de l'épuration des fumées
    10 04 09* déchets provenant de l'épuration des eaux de refroidissement contenant des hydrocarbures
    10 04 10 déchets provenant de l'épuration des eaux de refroidissement autres que ceux visés à la rubrique 10 04 09
    10 04 99 déchets non spécifiés ailleurs
    10 05 déchets provenant de la pyrométallurgie du zinc
    10 05 01 scories provenant de la production primaire et secondaire
    10 05 03* poussières de filtration des fumées
    10 05 04 autres fines et poussières
    10 05 05* déchets solides provenant de l'épuration des fumées
    10 05 06* boues et gâteaux de filtration provenant de l'épuration des fumées
    10 05 08* déchets provenant de l'épuration des eaux de refroidissement contenant des hydrocarbures
    10 05 09 déchets provenant de l'épuration des eaux de refroidissement autres que ceux visés à la rubrique 10 05 08
    10 05 10* crasses et écumes inflammables ou émettant, au contact de l'eau, des gaz inflammables en quantités dangereuses
    10 05 11 crasses et écumes autres que celles visées à la rubrique 10 05 10
    10 05 99 déchets non spécifiés ailleurs
    10 06 déchets provenant de la pyrométallurgie du cuivre
    10 06 01 scories provenant de la production primaire et secondaire
    10 06 02 crasses et écumes provenant de la production primaire et secondaire
    10 06 03* poussières de filtration des fumées
    10 06 04 autres fines et poussières
    10 06 06* déchets solides provenant de l'épuration des fumées
    10 06 07* boues et gâteaux de filtration provenant de l'épuration des fumées
    10 06 09* déchets provenant de l'épuration des eaux de refroidissement contenant des hydrocarbures
    10 06 10 déchets provenant de l'épuration des eaux de refroidissement autres que ceux visés à la rubrique 10 06 09
    10 06 99 déchets non spécifiés ailleurs
    10 07 déchets provenant de la pyrométallurgie de l'argent, de l'or et du platine
    10 07 01 scories provenant de la production primaire et secondaire
    10 07 02 crasses et écumes provenant de la production primaire et secondaire
    10 07 03 déchets solides provenant de l'épuration des fumées
    10 07 04 autres fines et poussières
    10 07 05 boues et gâteaux de filtration provenant de l'épuration des fumées
    10 07 07* déchets provenant de l'épuration des eaux de refroidissement contenant des hydrocarbures
    10 07 08 déchets provenant de l'épuration des eaux de refroidissement autres que ceux visés à la rubrique 10 07 07
    10 07 99 déchets non spécifiés ailleurs
    10 08 déchets provenant de la pyrométallurgie d'autres métaux non ferreux
    10 08 04 fines et poussières
    10 08 08* scories salées provenant de la production primaire et secondaire
    10 08 09 autres scories
    10 08 10* crasses et écumes inflammables ou émettant, au contact de l'eau, des gaz inflammables en quantités dangereuses
    10 08 11 crasses et écumes autres que celles visées à la rubrique 10 08 10
    10 08 12* déchets goudronnés provenant de la fabrication des anodes
    10 08 13 déchets carbonés provenant de la fabrication des anodes autres que ceux visés à la rubrique 10 08 12
    10 08 14 déchets d'anodes
    10 08 15* poussières de filtration des fumées contenant des substances dangereuses
    10 08 16 poussières de filtration des fumées autres que celles visées à la rubrique 10 08 15
    10 08 17* boues et gâteaux de filtration provenant de l'épuration des fumées contenant des substances dangereuses
    10 08 18 boues et gâteaux de filtration provenant de l'épuration des fumées autres que ceux visés à la rubrique 10 08 17
    10 08 19* déchets provenant de l'épuration des eaux de refroidissement contenant des hydrocarbures
    10 08 20 déchets provenant de l'épuration des eaux de refroidissement autres que ceux visés à la rubrique 10 08 19
    10 08 99 déchets non spécifiés ailleurs
    10 09 déchets de fonderie de métaux ferreux
    10 09 03 laitiers de four de fonderie
    10 09 05* noyaux et moules de fonderie n'ayant pas subi la coulée contenant des substances dangereuses
    10 09 06 noyaux et moules de fonderie n'ayant pas subi la coulée autres que ceux visés à la rubrique 10 09 05
    10 09 07* noyaux et moules de fonderie ayant subi la coulée contenant des substances dangereuses
    10 09 08 noyaux et moules de fonderie ayant subi la coulée autres que ceux visés à la rubrique 10 09 07
    10 09 09* poussières de filtration des fumées contenant des substances dangereuses
    10 09 10 poussières de filtration des fumées autres que celles visées à la rubrique 10 09 09
    10 09 11* autres fines contenant des substances dangereuses
    10 09 12 autres fines non visées à la rubrique 10 09 11
    10 09 13* déchets de liants contenant des substances dangereuses
    10 09 14 déchets de liants autres que ceux visés à la rubrique 10 09 13
    10 09 15* révélateur de criques usagé contenant des substances dangereuses
    10 09 16 révélateur de criques usagé autre que celui visé à la rubrique 10 09 15
    10 09 99 déchets non spécifiés ailleurs
    10 10 déchets de fonderie de métaux non ferreux
    10 10 03 laitiers de four de fonderie
    10 10 05* noyaux et moules de fonderie n'ayant pas subi la coulée contenant des substances dangereuses
    10 10 06 noyaux et moules de fonderie n'ayant pas subi la coulée autres que ceux visés à la rubrique 10 10 05
    10 10 07* noyaux et moules de fonderie ayant subi la coulée contenant des substances dangereuses
    10 10 08 noyaux et moules de fonderie ayant subi la coulée autres que ceux visés à la rubrique 10 10 07
    10 10 09* poussières de filtration des fumées contenant des substances dangereuses
    10 10 10 poussières de filtration des fumées autres que celles visées à la rubrique 10 10 09
    10 10 11* autres fines contenant des substances dangereuses
    10 10 12 autres fines non visées à la rubrique 10 10 11
    10 10 13* déchets de liants contenant des substances dangereuses
    10 10 14 déchets de liants autres que ceux visés à la rubrique 10 10 13
    10 10 15* révélateur de criques usagé contenant des substances dangereuses
    10 10 16 révélateur de criques usagé autre que celui visé à la rubrique 10 10 15
    10 10 99 déchets non spécifiés ailleurs
    10 11 déchets provenant de la fabrication du verre et des produits verriers
    10 11 03 déchets de matériaux à base de fibre de verre
    10 11 05 fines et poussières
    10 11 09* déchets de préparation avant cuisson contenant des substances dangereuses
    10 11 10 déchets de préparation avant cuisson autres que ceux visés à la rubrique 10 11 09
    10 11 11* petites particules de déchets de verre et poudre de verre contenant des métaux lourds (par exemple tubes cathodiques)
    10 11 12 déchets de verre autres que ceux visés à la rubrique 10 11 11
    10 11 13* boues de polissage et de meulage du verre contenant des substances dangereuses
    10 11 14 boues de polissage et de meulage du verre autres que celles visées à la rubrique 10 11 13
    10 11 15* déchets solides provenant de l'épuration des fumées contenant des substances dangereuses
    10 11 16 déchets solides provenant de l'épuration des fumées autres que ceux visés à la rubrique 10 11 15
    10 11 17* boues et gâteaux de filtration provenant de l'épuration des fumées contenant des substances dangereuses
    10 11 18 boues et gâteaux de filtration provenant de l'épuration des fumées autres que ceux visés à la rubrique 10 11 17
    10 11 19* déchets solides provenant du traitement in situ des effluents contenant des substances dangereuses
    10 11 20 déchets solides provenant du traitement in situ des effluents autres que ceux visés à la rubrique 10 11 19
    10 11 99 déchets non spécifiés ailleurs
    10 12 déchets provenant de la fabrication des produits en céramique, briques, carrelage et matériaux de construction
    10 12 01 déchets de préparation avant cuisson
    10 12 03 fines et poussières
    10 12 05 boues et gâteaux de filtration provenant de l'épuration des fumées
    10 12 06 moules déclassés
    10 12 08 déchets de produits en céramique, briques, carrelage et matériaux de construction (après cuisson)
    10 12 09* déchets solides provenant de l'épuration des fumées contenant des substances dangereuses
    10 12 10 déchets solides provenant de l'épuration des fumées autres que ceux visés à la rubrique 10 12 09
    10 12 11* déchets de glaçure contenant des métaux lourds
    10 12 12 déchets de glaçure autres que ceux visés à la rubrique 10 12 11
    10 12 13 boues provenant du traitement in situ des effluents
    10 12 99 déchets non spécifiés ailleurs
    10 13 déchets provenant de la fabrication de ciment, chaux et plâtre et d'articles et produits dérivés
    10 13 01 déchets de préparation avant cuisson
    10 13 04 déchets de calcination et d'hydratation de la chaux
    10 13 06 fines et poussières (sauf rubriques 10 13 12 et 10 13 13)
    10 13 07 boues et gâteaux de filtration provenant de l'épuration des fumées
    10 13 09* déchets provenant de la fabrication d'amiante-ciment contenant de l'amiante
    10 13 10 déchets provenant de la fabrication d'amiante-ciment autres que ceux visés à la rubrique 10 13 09
    10 13 11 déchets provenant de la fabrication de matériaux composites à base de ciment autres que ceux visés aux rubriques 10 13 09 et 10 13 10
    10 13 12* déchets solides provenant de l'épuration des fumées contenant des substances dangereuses
    10 13 13 déchets solides provenant de l'épuration des fumées autres que ceux visés à la rubrique 10 13 12
    10 13 14 déchets et boues de béton
    10 13 99 déchets non spécifiés ailleurs
    10 14 déchets de crématoires
    10 14 01* déchets provenant de l'épuration des fumées contenant du mercure
    11 DÉCHETS PROVENANT DU TRAITEMENT CHIMIQUE DE SURFACE ET DU REVÊTEMENT DES MÉTAUX ET AUTRES MATÉRIAUX, ET DE L'HYDROMÉTALLURGIE
    DES MÉTAUX NON FERREUX
    11 01 déchets provenant du traitement chimique de surface et du revêtement des métaux et autres matériaux (par exemple, procédés de galvanisation,
    de revêtement de zinc, de décapage, de gravure, de phosphatation, de dégraissage alcalin et d'anodisation)
    11 01 05* acides de décapage
    11 01 06* acides non spécifiés ailleurs
    11 01 07* bases de décapage
    11 01 08* boues de phosphatation
    11 01 09* boues et gâteaux de filtration contenant des substances dangereuses
    11 01 10 boues et gâteaux de filtration autres que ceux visés à la rubrique 11 01 09
    11 01 11* liquides aqueux de rinçage contenant des substances dangereuses
    11 01 12 liquides aqueux de rinçage autres que ceux visés à la rubrique 11 01 11
    11 01 13* déchets de dégraissage contenant des substances dangereuses
    11 01 14 déchets de dégraissage autres que ceux visés à la rubrique 11 01 13
    11 01 15* éluats et boues provenant des systèmes à membrane et des systèmes d'échange d'ions contenant des substances dangereuses
    11 01 16* résines échangeuses d'ions saturées ou usées
    11 01 98* autres déchets contenant des substances dangereuses
    11 01 99 déchets non spécifiés ailleurs
    11 02 déchets provenant des procédés hydrométallurgiques des métaux non ferreux
    11 02 02* boues provenant de l'hydrométallurgie du zinc (y compris jarosite et goethite)
    11 02 03 déchets provenant de la production d'anodes pour les procédés d'électrolyse aqueuse
    11 02 05* déchets provenant des procédés hydrométallurgiques du cuivre contenant des substances dangereuses
    11 02 06 déchets provenant des procédés hydrométallurgiques du cuivre autres que ceux visés à la rubrique 11 02 05
    11 02 07* autres déchets contenant des substances dangereuses
    11 02 99 déchets non spécifiés ailleurs
    11 03 boues et solides provenant de la trempe
    11 03 01* déchets cyanurés
    11 03 02* autres déchets
    11 05 déchets provenant de la galvanisation à chaud
    11 05 01 mattes
    11 05 02 cendres de zinc
    11 05 03* déchets solides provenant de l'épuration des fumées
    11 05 04* flux utilisé
    11 05 99 déchets non spécifiés ailleurs
    12 DÉCHETS PROVENANT DE LA MISE EN FORME ET DU TRAITEMENT PHYSIQUE ET MÉCANIQUE DE SURFACE DES MÉTAUX ET MATIÈRES PLASTIQUES
    12 01 déchets provenant de la mise en forme et du traitement mécanique et physique de surface des métaux et matières plastiques
    12 01 01 limaille et chutes de métaux ferreux
    12 01 02 fines et poussières de métaux ferreux
    12 01 03 limaille et chutes de métaux non ferreux
    12 01 04 fines et poussières de métaux non ferreux
    12 01 05 déchets de matières plastiques d'ébarbage et de tournage
    12 01 06* huiles d'usinage à base minérale contenant des halogènes (pas sous forme d'émulsions ou de solutions)
    12 01 07* huiles d'usinage à base minérale sans halogènes (pas sous forme d'émulsions ou de solutions)
    12 01 08* émulsions et solutions d'usinage contenant des halogènes
    12 01 09* émulsions et solutions d'usinage sans halogènes
    12 01 10* huiles d'usinage de synthèse
    12 01 12* déchets de cires et graisses
    12 01 13 déchets de soudure
    12 01 14* boues d'usinage contenant des substances dangereuses
    12 01 15 boues d'usinage autres que celles visées à la rubrique 12 01 14
    12 01 16* déchets de grenaillage contenant des substances dangereuses
    12 01 17 déchets de grenaillage autres que ceux visés à la rubrique 12 01 16
    12 01 18* boues métalliques (provenant du meulage et de l'affûtage) contenant des hydrocarbures
    12 01 19* huiles d'usinage facilement biodégradables
    12 01 20* déchets de meulage et matériaux de meulage contenant des substances dangereuses
    12 01 21 déchets de meulage et matériaux de meulage autres que ceux visés à la rubrique 12 01 20
    12 01 99 déchets non spécifiés ailleurs
    12 03 déchets provenant du dégraissage à l'eau et à la vapeur (sauf chapitre 11)
    12 03 01* liquides aqueux de nettoyage
    12 03 02* déchets du dégraissage à la vapeur
    13 HUILES ET COMBUSTIBLES LIQUIDES USAGÉS (sauf huiles alimentaires et huiles figurant aux chapitres 05, 12 et 19)
    13 01 huiles hydrauliques usagées
    13 01 01* huiles hydrauliques contenant des PCB
    13 01 04* huiles hydrauliques chlorées (émulsions)
    13 01 05* huiles hydrauliques non chlorées (émulsions)
    13 01 09* huiles hydrauliques chlorées à base minérale
    13 01 10* huiles hydrauliques non chlorées à base minérale
    13 01 11* huiles hydrauliques synthétiques
    13 01 12* huiles hydrauliques facilement biodégradables
    13 01 13* autres huiles hydrauliques
    13 02 huiles moteur, de boîte de vitesses et de lubrification usagées
    13 02 04* huiles moteur, de boîte de vitesses et de lubrification chlorées à base minérale
    13 02 05* huiles moteur, de boîte de vitesses et de lubrification non chlorées à base minérale
    13 02 06* huiles moteur, de boîte de vitesses et de lubrification synthétiques
    13 02 07* huiles moteur, de boîte de vitesses et de lubrification facilement biodégradables
    13 02 08* autres huiles moteur, de boîte de vitesses et de lubrification
    13 03 huiles isolantes et fluides caloporteurs usagés
    13 03 01* huiles isolantes et fluides caloporteurs contenant des PCB
    13 03 06* huiles isolantes et fluides caloporteurs chlorés à base minérale autres que ceux visés à la rubrique 13 03 01
    13 03 07* huiles isolantes et fluides caloporteurs non chlorés à base minérale
    13 03 08* huiles isolantes et fluides caloporteurs synthétiques
    13 03 09* huiles isolantes et fluides caloporteurs facilement biodégradables
    13 03 10* autres huiles isolantes et fluides caloporteurs
    13 04 hydrocarbures de fond de cale
    13 04 01* hydrocarbures de fond de cale provenant de la navigation fluviale
    13 04 02* hydrocarbures de fond de cale provenant de canalisations de môles
    13 04 03* hydrocarbures de fond de cale provenant d'un autre type de navigation
    13 05 contenu de séparateurs eau/hydrocarbures
    13 05 01* déchets solides provenant de dessableurs et de séparateurs eau/hydrocarbures
    13 05 02* boues provenant de séparateurs eau/hydrocarbures
    13 05 03* boues provenant de déshuileurs
    13 05 06* hydrocarbures provenant de séparateurs eau/hydrocarbures
    13 05 07* eau mélangée à des hydrocarbures provenant de séparateurs eau/hydrocarbures
    13 05 08* mélanges de déchets provenant de dessableurs et de séparateurs eau/hydrocarbures
    13 07 combustibles liquides usagés
    13 07 01* fuel oil et diesel
    13 07 02* essence
    13 07 03* autres combustibles (y compris mélanges)
    13 08 huiles usagées non spécifiées ailleurs
    13 08 01* boues ou émulsions de dessalage
    13 08 02* autres émulsions
    13 08 99* déchets non spécifiés ailleurs
    14 DÉCHETS DE SOLVANTS ORGANIQUES, D'AGENTS RÉFRIGÉRANTS ET PROPULSEURS (sauf chapitres 07 et 08)
    14 06 déchets de solvants, d'agents réfrigérants et d'agents propulseurs d'aérosols/de mousses organiques
    14 06 01* chlorofluorocarbones, HCFC, HFC
    14 06 02* autres solvants et mélanges de solvants halogénés
    14 06 03* autres solvants et mélanges de solvants
    14 06 04* boues ou déchets solides contenant des solvants halogénés
    14 06 05* boues ou déchets solides contenant d'autres solvants
    15 EMBALLAGES ET DÉCHETS D'EMBALLAGES, ABSORBANTS, CHIFFONS D'ESSUYAGE, MATÉRIAUX FILTRANTS ET VÊTEMENTS DE PROTECTION NON
    SPÉCIFIÉS AILLEURS
    15 01 emballages et déchets d'emballages (y compris les déchets d'emballages municipaux collectés séparément)
    15 01 01 emballages en papier/carton
    15 01 02 emballages en matières plastiques
    15 01 03 emballages en bois
    15 01 04 emballages métalliques
    15 01 05 emballages composites
    15 01 06 emballages en mélange
    15 01 07 emballages en verre
    15 01 09 emballages textiles
    15 01 10* emballages contenant des résidus de substances dangereuses ou contaminés par de tels résidus
    15 01 11* emballages métalliques contenant une matrice poreuse solide dangereuse (par exemple amiante), y compris des conteneurs à pression vides
    15 02 absorbants, matériaux filtrants, chiffons d'essuyage et vêtements de protection
    15 02 02* absorbants, matériaux filtrants (y compris les filtres à huile non spécifiés ailleurs), chiffons d'essuyage et vêtements de protection contaminés par des
    substances dangereuses
    15 02 03 absorbants, matériaux filtrants, chiffons d'essuyage et vêtements de protection autres que ceux visés à la rubrique 15 02 02
    16 DÉCHETS NON DÉCRITS AILLEURS DANS LA LISTE
    16 01 véhicules hors d'usage de différents moyens de transport (y compris machines tous terrains) et déchets provenant du démontage de véhicules hors
    d'usage et de l'entretien de véhicules (sauf chapitres 13, 14, et sections 16 06 et 16 08)
    16 01 03 pneus hors d'usage
    16 01 04* véhicules hors d'usage
    16 01 06 véhicules hors d'usage ne contenant ni liquides ni autres composants dangereux
    16 01 07* filtres à huile
    16 01 08* composants contenant du mercure
    16 01 09* composants contenant des PCB
    16 01 10* composants explosifs (par exemple coussins gonflables de sécurité)
    16 01 11* patins de freins contenant de l'amiante
    16 01 12 patins de freins autres que ceux visés à la rubrique 16 01 11
    16 01 13* liquides de frein
    16 01 14* antigels contenant des substances dangereuses
    16 01 15 antigels autres que ceux visés à la rubrique 16 01 14
    16 01 16 réservoirs de gaz liquéfié
    16 01 17 métaux ferreux
    16 01 18 métaux non ferreux
    16 01 19 matières plastiques
    16 01 20 verre
    16 01 21* composants dangereux autres que ceux visés aux rubriques 16 01 07 à 16 01 11, 16 01 13 et 16 01 14
    16 01 22 composants non spécifiés ailleurs
    16 01 99 déchets non spécifiés ailleurs
    16 02 déchets provenant d'équipements électriques ou électroniques
    16 02 09* transformateurs et accumulateurs contenant des PCB
    16 02 10* équipements mis au rebut contenant des PCB ou contaminés par de telles substances autres que ceux visés à la rubrique 16 02 09
    16 02 11* équipements mis au rebut contenant des chlorofluorocarbones, des HCFC ou des HFC
    16 02 12* équipements mis au rebut contenant de l'amiante libre
    16 02 13* équipements mis au rebut contenant des composants dangereux (3) autres que ceux visés aux rubriques 16 02 09 à 16 02 12
    16 02 14 équipements mis au rebut autres que ceux visés aux rubriques 16 02 09 à 16 02 13
    16 02 15* composants dangereux retirés des équipements mis au rebut
    16 02 16 composants retirés des équipements mis au rebut autres que ceux visés à la rubrique 16 02 15
    16 03 loupés de fabrication et produits non utilisés
    16 03 03* déchets d'origine minérale contenant des substances dangereuses
    16 03 04 déchets d'origine minérale autres que ceux visés à la rubrique 16 03 03
    16 03 05* déchets d'origine organique contenant des substances dangereuses
    16 03 06 déchets d'origine organique autres que ceux visés à la rubrique 16 03 05
    16 03 07* mercure métallique
    16 04 déchets d'explosifs
    16 04 01* déchets de munitions
    16 04 02* déchets de feux d'artifice
    16 04 03* autres déchets d'explosifs
    16 05 gaz en récipients à pression et produits chimiques mis au rebut
    16 05 04* gaz en récipients à pression (y compris les halons) contenant des substances dangereuses
    16 05 05 gaz en récipients à pression autres que ceux visés à la rubrique 16 05 04
    16 05 06* produits chimiques de laboratoire à base de ou contenant des substances dangereuses, y compris les mélanges de produits chimiques de laboratoire
    16 05 07* produits chimiques d'origine minérale à base de ou contenant des substances dangereuses, mis au rebut
    16 05 08* produits chimiques d'origine organique à base de ou contenant des substances dangereuses, mis au rebut
    16 05 09 produits chimiques mis au rebut autres que ceux visés aux rubriques 16 05 06, 16 05 07 ou 16 05 08
    16 06 piles et accumulateurs
    16 06 01* accumulateurs au plomb
    16 06 02* accumulateurs Ni-Cd
    16 06 03* piles contenant du mercure
    16 06 04 piles alcalines (sauf rubrique 16 06 03)
    16 06 05 autres piles et accumulateurs
    16 06 06* électrolytes de piles et accumulateurs collectés séparément
    16 07 déchets provenant du nettoyage de cuves et fûts de stockage et de transport (sauf chapitres 05 et 13)
    16 07 08* déchets contenant des hydrocarbures
    16 07 09* déchets contenant d'autres substances dangereuses
    16 07 99 déchets non spécifiés ailleurs
    16 08 catalyseurs usés
    16 08 01 catalyseurs usés contenant de l'or, de l'argent, du rhénium, du rhodium, du palladium, de l'iridium ou du platine (sauf rubrique 16 08 07)
    16 08 02* catalyseurs usés contenant des métaux ou composés de métaux de transition dangereux
    16 08 03 catalyseurs usés contenant des métaux ou composés de métaux de transition non spécifiés ailleurs
    16 08 04 catalyseurs usés de craquage catalytique sur lit fluide (sauf rubrique 16 08 07)
    16 08 05* catalyseurs usés contenant de l'acide phosphorique
    16 08 06* liquides usés employés comme catalyseurs
    16 08 07* catalyseurs usés contaminés par des substances dangereuses
    16 09 substances oxydantes
    16 09 01* permanganates, par exemple, permanganate de potassium
    16 09 02* chromates, par exemple, chromate de potassium, dichromate de sodium ou de potassium
    16 09 03* peroxydes, par exemple, peroxyde d'hydrogène
    16 09 04* substances oxydantes non spécifiées ailleurs
    16 10 déchets liquides aqueux destinés à un traitement hors site
    16 10 01* déchets liquides aqueux contenant des substances dangereuses
    16 10 02 déchets liquides aqueux autres que ceux visés à la rubrique 16 10 01
    16 10 03* concentrés aqueux contenant des substances dangereuses
    16 10 04 concentrés aqueux autres que ceux visés à la rubrique 16 10 03
    16 11 déchets de revêtements de fours et réfractaires
    16 11 01* revêtements de fours et réfractaires à base de carbone provenant de procédés métallurgiques contenant des substances dangereuses
    16 11 02 revêtements de fours et réfractaires à base de carbone provenant de procédés métallurgiques autres que ceux visés à la rubrique 16 11 01
    16 11 03* autres revêtements de fours et réfractaires provenant de procédés métallurgiques contenant des substances dangereuses
    16 11 04 autres revêtements de fours et réfractaires provenant de procédés métallurgiques non visés à la rubrique 16 11 03
    16 11 05* revêtements de fours et réfractaires provenant de procédés non métallurgiques contenant des substances dangereuses
    16 11 06 revêtements de fours et réfractaires provenant de procédés non métallurgiques autres que ceux visés à la rubrique 16 11 05
    17 DÉCHETS DE CONSTRUCTION ET DE DÉMOLITION (Y COMPRIS DÉBLAIS PROVENANT DE SITES CONTAMINÉS)
    17 01 béton, briques, tuiles et céramiques
    17 01 01 béton
    17 01 02 briques
    17 01 03 tuiles et céramiques
    17 01 06* mélanges ou fractions séparées de béton, briques, tuiles et céramiques contenant des substances dangereuses
    17 01 07 mélanges de béton, briques, tuiles et céramiques autres que ceux visés à la rubrique 17 01 06
    17 02 bois, verre et matières plastiques
    17 02 01 bois
    17 02 02 verre
    17 02 03 matières plastiques
    17 02 04* bois, verre et matières plastiques contenant des substances dangereuses ou contaminés par de telles substances
    17 03 mélanges bitumineux, goudron et produits goudronnés
    17 03 01* mélanges bitumineux contenant du goudron
    17 03 02 mélanges bitumineux autres que ceux visés à la rubrique 17 03 01
    17 03 03* goudron et produits goudronnés
    17 04 métaux (y compris leurs alliages)
    17 04 01 cuivre, bronze, laiton
    17 04 02 aluminium
    17 04 03 plomb
    17 04 04 zinc
    17 04 05 fer et acier
    17 04 06 étain
    17 04 07 métaux en mélange
    17 04 09* déchets métalliques contaminés par des substances dangereuses
    17 04 10* câbles contenant des hydrocarbures, du goudron ou d'autres substances dangereuses
    17 04 11 câbles autres que ceux visés à la rubrique 17 04 10
    17 05 terres (y compris déblais provenant de sites contaminés), cailloux et boues de dragage
    17 05 03* terres et cailloux contenant des substances dangereuses
    17 05 04 terres et cailloux autres que ceux visés à la rubrique 17 05 03
    17 05 05* boues de dragage contenant des substances dangereuses
    17 05 06 boues de dragage autres que celles visées à la rubrique 17 05 05
    17 05 07* ballast de voie contenant des substances dangereuses
    17 05 08 ballast de voie autre que celui visé à la rubrique 17 05 07
    17 06 matériaux d'isolation et matériaux de construction contenant de l'amiante
    17 06 01* matériaux d'isolation contenant de l'amiante
    17 06 03* autres matériaux d'isolation à base de ou contenant des substances dangereuses
    17 06 04 matériaux d'isolation autres que ceux visés aux rubriques 17 06 01 et 17 06 03
    17 06 05* matériaux de construction contenant de l'amiante
    17 08 matériaux de construction à base de gypse
    17 08 01* matériaux de construction à base de gypse contaminés par des substances dangereuses
    17 08 02 matériaux de construction à base de gypse autres que ceux visés à la rubrique 17 08 01
    17 09 autres déchets de construction et de démolition
    17 09 01* déchets de construction et de démolition contenant du mercure
    17 09 02* déchets de construction et de démolition contenant des PCB (par exemple, mastics, sols à base de résines, double vitrage, condensateurs, contenant des
    PCB)
    17 09 03* autres déchets de construction et de démolition (y compris en mélange) contenant des substances dangereuses
    17 09 04 déchets de construction et de démolition en mélange autres que ceux visés aux rubriques 17 09 01, 17 09 02 et 17 09 03
    18 DÉCHETS PROVENANT DES SOINS MÉDICAUX OU VÉTÉRINAIRES ET/OU DE LA RECHERCHE ASSOCIÉE (sauf déchets de cuisine et de restauration ne
    provenant pas directement des soins médicaux)
    18 01 déchets provenant des maternités, du diagnostic, du traitement ou de la prévention des maladies de l'homme
    18 01 01 objets piquants et coupants (sauf rubrique 18 01 03)
    18 01 02 déchets anatomiques et organes, y compris sacs de sang et réserves de sang (sauf rubrique 18 01 03)
    18 01 03* déchets dont la collecte et l'élimination font l'objet de prescriptions particulières vis-à-vis des risques d'infection
    18 01 04 déchets dont la collecte et l'élimination ne font pas l'objet de prescriptions particulières vis-à-vis des risques d'infection (par exemple vêtements, plâtres,
    draps, vêtements jetables, langes)
    18 01 06* produits chimiques à base de ou contenant des substances dangereuses
    18 01 07 produits chimiques autres que ceux visés à la rubrique 18 01 06
    18 01 08* médicaments cytotoxiques et cytostatiques
    18 01 09 médicaments autres que ceux visés à la rubrique 18 01 08
    18 01 10* déchets d'amalgame dentaire
    18 02 déchets provenant de la recherche, du diagnostic, du traitement ou de la prévention des maladies des animaux
    18 02 01 objets piquants et coupants (sauf rubrique 18 02 02)
    18 02 02* déchets dont la collecte et l'élimination font l'objet de prescriptions particulières vis-à-vis des risques d'infection
    18 02 03 déchets dont la collecte et l'élimination ne font pas l'objet de prescriptions particulières vis-à-vis des risques d'infection
    18 02 05* produits chimiques à base de ou contenant des substances dangereuses
    18 02 06 produits chimiques autres que ceux visés à la rubrique 18 02 05
    18 02 07* médicaments cytotoxiques et cytostatiques
    18 02 08 médicaments autres que ceux visés à la rubrique 18 02 07
    19 DÉCHETS PROVENANT DES INSTALLATIONS DE GESTION DES DÉCHETS, DES STATIONS D'ÉPURATION DES EAUX USÉES HORS SITE ET DE LA
    PRÉPARATION D'EAU DESTINÉE À LA CONSOMMATION HUMAINE ET D'EAU À USAGE INDUSTRIEL
    19 01 déchets de l'incinération ou de la pyrolyse de déchets
    19 01 02 déchets de déferraillage des mâchefers
    19 01 05* gâteaux de filtration provenant de l'épuration des fumées
    19 01 06* déchets liquides aqueux provenant de l'épuration des fumées et autres déchets liquides aqueux
    19 01 07* déchets solides provenant de l'épuration des fumées
    19 01 10* charbon actif usé provenant de l'épuration des gaz de fumées
    19 01 11* mâchefers contenant des substances dangereuses
    19 01 12 mâchefers autres que ceux visés à la rubrique 19 01 11
    19 01 13* cendres volantes contenant des substances dangereuses
    19 01 14 cendres volantes autres que celles visées à la rubrique 19 01 13
    19 01 15* cendres sous chaudière contenant des substances dangereuses
    19 01 16 cendres sous chaudière autres que celles visées à la rubrique 19 01 15
    19 01 17* déchets de pyrolyse contenant des substances dangereuses
    19 01 18 déchets de pyrolyse autres que ceux visés à la rubrique 19 01 17
    19 01 19 sables provenant de lits fluidisés
    19 01 99 déchets non spécifiés ailleurs
    19 02 déchets provenant des traitements physico-chimiques des déchets (notamment, déchromatation, décyanuration, neutralisation)
    19 02 03 déchets prémélangés composés seulement de déchets non dangereux
    19 02 04* déchets prémélangés contenant au moins un déchet dangereux
    19 02 05* boues provenant des traitements physico-chimiques contenant des substances dangereuses
    19 02 06 boues provenant des traitements physico-chimiques autres que celles visées à la rubrique 19 02 05
    19 02 07* hydrocarbures et concentrés provenant d'une séparation
    19 02 08* déchets combustibles liquides contenant des substances dangereuses
    19 02 09* déchets combustibles solides contenant des substances dangereuses
    19 02 10 déchets combustibles autres que ceux visés aux rubriques 19 02 08 et 19 02 09
    19 02 11* autres déchets contenant des substances dangereuses
    19 02 99 déchets non spécifiés ailleurs
    19 03 déchets stabilisés/solidifiés
    19 03 04* déchets marqués comme dangereux partiellement stabilisés, autres que ceux visés à la rubrique 19 03 08
    19 03 05 déchets stabilisés autres que ceux visés à la rubrique 19 03 04
    19 03 06* déchets catalogués comme dangereux, solidifiés
    19 03 07 déchets solidifiés autres que ceux visés à la rubrique 19 03 06
    19 03 08* mercure partiellement stabilisé
    19 04 déchets vitrifiés et déchets provenant de la vitrification
    19 04 01 déchets vitrifiés
    19 04 02* cendres volantes et autres déchets du traitement des gaz de fumée
    19 04 03* phase solide non vitrifiée
    19 04 04 déchets liquides aqueux provenant de la trempe des déchets vitrifiés
    19 05 déchets de compostage
    19 05 01 fraction non compostée des déchets municipaux et assimilés
    19 05 02 fraction non compostée des déchets animaux et végétaux
    19 05 03 compost déclassé
    19 05 99 déchets non spécifiés ailleurs
    19 06 déchets provenant du traitement anaérobie des déchets
    19 06 03 liqueurs provenant du traitement anaérobie des déchets municipaux
    19 06 04 digestats provenant du traitement anaérobie des déchets municipaux
    19 06 05 liqueurs provenant du traitement anaérobie des déchets animaux et végétaux
    19 06 06 digestats provenant du traitement anaérobie des déchets animaux et végétaux
    19 06 99 déchets non spécifiés ailleurs
    19 07 lixiviats de décharges
    19 07 02* lixiviats de décharges contenant des substances dangereuses
    19 07 03 lixiviats de décharges autres que ceux visés à la rubrique 19 07 02
    19 08 déchets provenant d'installations de traitement des eaux usées non spécifiés ailleurs
    19 08 01 déchets de dégrillage
    19 08 02 déchets de dessablage
    19 08 05 boues provenant du traitement des eaux usées urbaines
    19 08 06* résines échangeuses d'ions saturées ou usées
    19 08 07* solutions et boues provenant de la régénération des échangeurs d'ions
    19 08 08* déchets provenant des systèmes à membrane contenant des métaux lourds
    19 08 09 mélanges de graisse et d'huile provenant de la séparation huile/eaux usées contenant seulement des huiles et graisses alimentaires
    19 08 10* mélanges de graisse et d'huile provenant de la séparation huile/eaux usées autres que ceux visés à la rubrique 19 08 09
    19 08 11* boues contenant des substances dangereuses provenant du traitement biologique des eaux usées industrielles
    19 08 12 boues provenant du traitement biologique des eaux usées industrielles autres que celles visées à la rubrique 19 08 11
    19 08 13* boues contenant des substances dangereuses provenant d'autres traitements des eaux usées industrielles
    19 08 14 boues provenant d'autres traitements des eaux usées industrielles autres que celles visées à la rubrique 19 08 13
    19 08 99 déchets non spécifiés ailleurs
    19 09 déchets provenant de la préparation d'eau destinée à la consommation humaine ou d'eau à usage industriel
    19 09 01 déchets solides de première filtration et de dégrillage
    19 09 02 boues de clarification de l'eau
    19 09 03 boues de décarbonatation
    19 09 04 charbon actif usé
    19 09 05 résines échangeuses d'ions saturées ou usées
    19 09 06 solutions et boues provenant de la régénération des échangeurs d'ions
    19 09 99 déchets non spécifiés ailleurs
    19 10 déchets provenant du broyage de déchets contenant des métaux
    19 10 01 déchets de fer ou d'acier
    19 10 02 déchets de métaux non ferreux
    19 10 03* fraction légère des résidus de broyage et poussières contenant des substances dangereuses
    19 10 04 fraction légère des résidus de broyage et poussières autres que celles visées à la rubrique 19 10 03
    19 10 05* autres fractions contenant des substances dangereuses
    19 10 06 autres fractions autres que celles visées à la rubrique 19 10 05
    19 11 déchets provenant de la régénération de l'huile
    19 11 01* argiles de filtration usées
    19 11 02* goudrons acides
    19 11 03* déchets liquides aqueux
    19 11 04* déchets provenant du nettoyage d'hydrocarbures avec des bases
    19 11 05* boues provenant du traitement in situ des effluents contenant des substances dangereuses
    19 11 06 boues provenant du traitement in situ des effluents autres que celles visées à la rubrique 19 11 05
    19 11 07* déchets provenant de l'épuration des gaz de combustion
    19 11 99 déchets non spécifiés ailleurs
    19 12 déchets provenant du traitement mécanique des déchets (par exemple, tri, broyage, compactage, granulation) non spécifiés ailleurs
    19 12 01 papier et carton
    19 12 02 métaux ferreux
    19 12 03 métaux non ferreux
    19 12 04 matières plastiques et caoutchouc
    19 12 05 verre
    19 12 06* bois contenant des substances dangereuses
    19 12 07 bois autres que ceux visés à la rubrique 19 12 06
    19 12 08 textiles
    19 12 09 minéraux (par exemple sable, cailloux)
    19 12 10 déchets combustibles (combustible issu de déchets)
    19 12 11* autres déchets (y compris mélanges) provenant du traitement mécanique des déchets contenant des substances dangereuses
    19 12 12 autres déchets (y compris mélanges) provenant du traitement mécanique des déchets autres que ceux visés à la rubrique 19 12 11
    19 13 déchets provenant de la décontamination des sols et des eaux souterraines
    19 13 01* déchets solides provenant de la décontamination des sols contenant des substances dangereuses
    19 13 02 déchets solides provenant de la décontamination des sols autres que ceux visés à la rubrique 19 13 01
    19 13 03* boues provenant de la décontamination des sols contenant des substances dangereuses
    19 13 04 boues provenant de la décontamination des sols autres que celles visées à la rubrique 19 13 03
    19 13 05* boues provenant de la décontamination des eaux souterraines contenant des substances dangereuses
    19 13 06 boues provenant de la décontamination des eaux souterraines autres que celles visées à la rubrique 19 13 05
    19 13 07* déchets liquides aqueux et concentrés aqueux provenant de la décontamination des eaux souterraines contenant des substances dangereuses
    19 13 08 déchets liquides aqueux et concentrés aqueux provenant de la décontamination des eaux souterraines autres que ceux visés à la rubrique 19 13 07
    20 DÉCHETS MUNICIPAUX (DÉCHETS MÉNAGERS ET DÉCHETS ASSIMILÉS PROVENANT DES COMMERCES, DES INDUSTRIES ET DES ADMINISTRATIONS), Y
    COMPRIS LES FRACTIONS COLLECTÉES SÉPARÉMENT
    20 01 fractions collectées séparément (sauf section 15 01)
    20 01 01 papier et carton
    20 01 02 verre
    20 01 08 déchets de cuisine et de cantine biodégradables
    20 01 10 vêtements
    20 01 11 textiles
    20 01 13* solvants
    20 01 14* acides
    20 01 15* déchets basiques
    20 01 17* produits chimiques de la photographie
    20 01 19* pesticides
    20 01 21* tubes fluorescents et autres déchets contenant du mercure
    20 01 23* équipements mis au rebut contenant des chlorofluorocarbones
    20 01 25 huiles et matières grasses alimentaires
    20 01 26* huiles et matières grasses autres que celles visées à la rubrique 20 01 25
    20 01 27* peinture, encres, colles et résines contenant des substances dangereuses
    20 01 28 peinture, encres, colles et résines autres que celles visées à la rubrique 20 01 27
    20 01 29* détergents contenant des substances dangereuses
    20 01 30 détergents autres que ceux visés à la rubrique 20 01 29
    20 01 31* médicaments cytotoxiques et cytostatiques
    20 01 32 médicaments autres que ceux visés à la rubrique 20 01 31
    20 01 33* piles et accumulateurs visés aux rubriques 16 06 01, 16 06 02 ou 16 06 03 et piles et accumulateurs non triés contenant ces piles
    20 01 34 piles et accumulateurs autres que ceux visés à la rubrique 20 01 33
    20 01 35* équipements électriques et électroniques mis au rebut contenant des composants dangereux, autres que ceux visés aux rubriques 20 01 21 et 20 01 23 (3)
    20 01 36 équipements électriques et électroniques mis au rebut autres que ceux visés aux rubriques 20 01 21, 20 01 23 et 20 01 35
    20 01 37* bois contenant des substances dangereuses
    20 01 38 bois autres que ceux visés à la rubrique 20 01 37
    20 01 39 matières plastiques
    20 01 40 métaux
    20 01 41 déchets provenant du ramonage de cheminée
    20 01 99 autres fractions non spécifiées ailleurs
    20 02 déchets de jardins et de parcs (y compris les déchets de cimetière)
    20 02 01 déchets biodégradables
    20 02 02 terres et pierres
    20 02 03 autres déchets non biodégradables
    20 03 autres déchets municipaux
    20 03 01 déchets municipaux en mélange
    20 03 02 déchets de marchés
    20 03 03 déchets de nettoyage des rues
    20 03 04 boues de fosses septiques
    20 03 06 déchets provenant du nettoyage des égouts
    20 03 07 déchets encombrants
    20 03 99 déchets municipaux non spécifiés ailleurs

"""


def get_all_ceds(text):
    # Pattern pour trouver les codes CED (3 couples de 2 chiffres avec ou sans astérisque)
    pattern = r'\b(\d{2}\s+\d{2}\s+\d{2})\*?\b'
    
    # Trouver tous les codes CED dans le texte
    codes = re.findall(pattern, text)
    
    # Ajouter l'astérisque si elle existe dans le texte original
    codes_with_asterisk = []
    for code in codes:
        if code + '*' in text:
            codes_with_asterisk.append(code + '*')
        else:
            codes_with_asterisk.append(code)
    
    return codes_with_asterisk

# Exemple d'utilisation
if __name__ == "__main__":
    codes = get_all_ceds(text)
    print("Liste des codes CED trouvés :")
    print(codes)
    
    # Sauvegarder la liste dans un fichier
    with open('codes_ced.txt', 'w', encoding='utf-8') as f:
        for code in codes:
            f.write(code + '\n')
    print("\nLes codes ont été sauvegardés dans le fichier 'codes_ced.txt'")


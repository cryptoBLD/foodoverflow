# Projektbericht Foodoverflow
### Erreichte Resultate
* 3 zufällige Rezepte werden angezeigt.
* Man kann mit verschiedenen Filtern nach Rezepten suchen.
* Details einzelner Rezepte können angezeigt werden.
* Man kann sich mit seinem Namen Anmelden(NUR MÖGLICH WENN EIN ZUGEHÖRIGER TOKEN EXISTIERT).
* Man kann eine Bewertung schreiben.
* Vorherige Bewertungen zum Rezept werden angezeigt.

## Dokumentation
### Startseite:
Auf der Startseite werden 3 zufällige Rezepte angezeigt. Wenn man mit dem Mauszeiger über ein Rezept platziert wird der
Name und eine durchschnittliche Bewertung angezeigt. Falls es noch keine existiert wird "N/A" angezeigt.
Unterhalb der Rezepte wird eine Suchleiste angezeigt, bei welcher man nach verschiedenen Kategorien Filtern kann.
Auch wird einem User ein Token zugewiesen, welches das generelle Token der Webseite ist. Dieses kann man später noch ändern.

### Suchseite:
Auf der Suchseite werden die Resultate der Suche, welche auf der Startseite getätigt wurde, angezeigt.
Wenn man mit dem Mauszeiger über ein Rezept platziert wird der Name und eine durchschnittliche Bewertung angezeigt. Falls es noch keine existiert wird "N/A" angezeigt.

### Detailseite
Auf der Detailseite wird das Rezept angezeigt mit einem Bild, den Zutaten und der Anleitung.
Unterhalb des Rezepts kommt der Paragraph mit den Bewertungen. Zuerst gibt es einen Login Button wo man sich dann mit Namen(welcher sich in der Tokens JSON Datei befindet) einloggen kann und auch unter dem Namen eine Bewertung hinterlassen kann. Alle Bewertungen werden dann unterhalb angezeigt mit der Nachricht und den Sternen.

### Loginseite
Auf dieser Seite kann man sich einloggen. Nach dem Einloggen wird einem ein Token zugeteilt.

### Struktur der Webseite
Die Webseite ist folgendermassen Strukturiert
* **Homepage**
  * Willkommens Text
  * Drei zufällige Rezepte
  * Suchleiste
  * Filter
* **Search-page**
    * Such Resultate
* **Details-page**
    * Rezept name
    * Zutaten dargestellt in einer Liste
    * Rezept Bild
    * Rezept Anleitung
    * Rückmeldungsformular
    * Andere Rückmeldung soweit sie existieren
* **login-page**
    * Login mit Namen

## Rückblick
Wir haben all unsere Ziele erreicht und haben sogar ein Neues hinzugefügt. Wir waren innerhalb der Gruppe gut organisiert und wussten immer was wir tun sollten. 
Das Arbeiten mit Flask war sehr interessant und lehrreich. Wir haben die Arbeit gut aufgeteilt und hatten deshalb nie Zeitprobleme.
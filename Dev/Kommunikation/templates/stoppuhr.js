/*********** Java-Script **********/

var dStartTime;       // Startzeit
var bRunning = false; // wird true, wenn Stoppuhr gestartet wird

// Start/StopTimer - startet bzw. haelt die Stoppuhr an

function StartTimer()
  {
  bRunning = true;          // merken, dass Stoppuhr laeuft
  dStartTime = new Date();  // Startzeit merken
  ShowTime();               // Startzeit anzeigen (0:00:00)
  }

function StopTimer()
  {
  bRunning = false;         // Stoppuhr als angehalten merken
  }

// ShowTime() zeigt die aktuelle Zeit der Stoppuhr an und veranlasst,
// dass diese Routine automatisch nach Ablauf von 1 Sekunde wieder
// aufgerufen wird - ausser die Stoppuhr wurde zwischenzeitlich 
// angehalten

function ShowTime()
  {
  if( !bRunning ) // Stoppuhr angehalten?
    return;
    
  var dDeltaTime = new Date();  // Variable dDeltaTime als Datumsvariable deklarieren
  dDeltaTime.setTime( new Date() - dStartTime ); // Differenz: Aktuelle Zeit und Startzeit

  var sMin = dDeltaTime.getMinutes(); // Minutenanteil der Differenz
  var sSec = dDeltaTime.getSeconds(); // Sekundenanteil der Differenz
  
  // Die Stunden werden als ganze Zahl der Differenz dividiert durch Sekunden
  // pro Stunde ausgerechnet. Dabei kann es natuerlich auch zu Werten groesser
  // als 24 fuehren, das ist so beabsichtigt.
  
  var sHours = Math.floor( dDeltaTime / 3600000 );

  // Bei der Umwandlung in eine ansprechende Darstellung der Stoppuhrzeit
  // sollen immer zwei Ziffern fuer die Sekunden und Minuten angezeigt
  // werden, sind es weniger als 10 Minuten bzw. Sekunden, wird eine Null
  // vor die Ausgabe eingefuegt.
   
  sMin = ( sMin < 10 ) ? "0" + sMin : sMin;
  sSec = ( sSec < 10 ) ? "0" + sSec : sSec;

  // Die Anzeige der Uhrzeit wird direkt als Wert des Texteingabefeldes sTime
  // eingetragen
  
  document.control.sTime.value = sHours + ":" + sMin + ":" + sSec;
  //document.forms[0].sTime.value = sHours + ":" + sMin + ":" + sSec;
  
  // Aufruf der Systemroutine setTimeout: nach 1000 Millisekunden (= 1 Sekunde)
  // soll wieder die Funktion ShowTime() aufgerufen werden.
  
  setTimeout('ShowTime()', 1000);
  }

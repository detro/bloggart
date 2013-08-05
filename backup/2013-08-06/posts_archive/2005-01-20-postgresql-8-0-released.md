---
layout: post
author: detro
published: true
title: "PostgreSQL 8.0 released"
tags: [uncategorized]
date: "2005-01-20 01:32:31"
published: "2005-01-20 01:32:31"
updated: "2005-01-20 01:32:31"
permalink: /2005/01/20/postgresql-80-released/
---

<div style="clear:both;"></div>Il link rimanda al "Press Kit" in Italiano.<br />Quì il link in inglese: <a href="http://www.postgresql.org/about/press/presskit80.html" title="presskit">http://www.postgresql.org/about/press/presskit80.html</a>.<br /><br /><img src="http://www.bimboflap.it/risorse/servizi/coloriamo/B.N/elefante.gif" alt="Elephant" align="right" width="40%" height="40%" /><blockquote>NY, NY: 19 Gennaio 2005 - Il Gruppo di Sviluppo Globale di PostgreSQL ha rilasciato la versione 8.0 del sistema di gestione di basi dati relazionali e ad oggetti PostgreSQL, rinforzando la sua posizione di server di database open source più avanzato al mondo. Questa versione include caratteristiche presenti, in precedenza, solamente sui server di database proprietari e molto costosi, e si prevede un sostanziale aumento nell'adozione di PostgreSQL sia da parte degli utenti che dei distributori di software.<br /><br />Oltre a significative migliorie nella scalabilità, nelle funzionalità e nelle prestazioni, PostgreSQL 8.0 dimostra l'ineguagliabile velocità di sviluppo caratteristica dell'Open Source. Più di una dozzina di compagnie, comprendendo Red Hat, Fujitsu, Afilias, Software Research Associates, Inc., 2nd Quadrant, e Command Prompt, Inc., insieme a centinaia di sviluppatori indipendenti, hanno contribuito ad aggiungere importanti funzionalità alla versione 8.0, più di quante se ne siano viste in precedenti versioni.<br /><br />"Crediamo che queste caratteristiche orientate alle imprese attrarranno un gran numero di nuovi utenti su PostgreSQL." ha affermato Takayuki Nakazawa, responsabile del gruppo di sviluppo di database open source per la Fujitsu. "Fujitsu è orgogliosa di sponsorizzare i contributi allo sviluppo di PostgreSQL e di lavorare con la sua comunità. Il nostro scopo è rendere PostgreSQL il Server di Database di riferimento."<br /><br />Queste nuove caratteristiche comprendono:<br /><ul><br />    <li>Supporto nativo per Windows: PostgreSQL adesso funziona nativamente sotto sistemi Windows e non ha più bisogno di uno strato di emulazione software. Questo fornisce prestazioni molto migliori rispetto a versioni precedenti, ed offre una valida alternativa ai database proprietari per fornitori di software indipendenti, utenti aziendali e singoli sviluppatori sotto Windows.<br />    <li>Punti di salvataggio (Savepoints): questa caratteristica che fa parte dello standard SQL permette l'annullamento di singole parti di una transazione senza dover interrompere l'intera operazione. È di beneficio agli sviluppatori di applicazioni business che possono aver bisogno di transazioni complesse con possibilità di recupero dagli errori.<br />    <li>Ripristino da un punto nel tempo (Point in time recovery): questa caratteristica permette il completo recupero dei dati a partire dagli archivi delle transazioni, che vengono scritti ed archiviati automaticamente e continuamente. Fornisce una alternativa attesa da lungo tempo alle copie di sicurezza giornaliere od orarie, per servizi ad alta criticità dei dati basati su PostgreSQL.<br />    <li>Spazi di tabella (Tablespaces): fondamentali per l'amministrazione di sistemi per l'immagazzinamento di dati delle dimensioni di svariati gigabyte, i tablespace permettono la memorizzazione di tabelle ed indici su dischi dedicati o su insiemi di questi, migliorando i tempi di esecuzione delle query.<br />    <li>Migliorie nell'utilizzo della memoria e dell'I/O: l'utilizzo di queste risorse è stato ottimizzato grazie all'uso di algoritmi di Cache con rimpiazzo adattivo, al nuovo algoritmo di scrittura in background, ed alla nuova caratteristica di riutilizzo degli spazi ritardata (vacuum delay). Questo permetterà carichi più prevedibili e sostanzialmente in prestazioni migliori durante i picchi di massimo utilizzo.<br /></ul><br /><br />Javier Soltero, Architetto Capo alla Hyperic LLC ha affermato: "PostgreSQL 8.0 ci fornisce un alto grado di concorrenza e risultati restituiti velocemente, cose entrambi richieste dal nostro prodotto di controllo HQ. Il fatto di avere PostgreSQL nativo sotto Windows significa che adesso possiamo includerlo nel nostro prodotto e beneficiare sia della sua scalabilità che delle sue prestazioni, così come della sua licenza, che ci permette di includerlo nelle nostre distribuzioni senza alcun obbligo commerciale."<br /><br />In aggiunta alle molte caratteristiche che lo accompagnano, PostgreSQL è stato migliorato anche dall'accelerato sviluppo di aggiunte e componenti opzionali lungo tutto il corso dell'anno scorso. Lo strumento per la replicazione Slony-I e l'utilità di pooling/brokering di connessioni pgPool vengono già usate per insiemi di server ad alta disponibilità. Diversi linguaggi per la scrittura di stored procedure sono stati aggiunti o migliorati, e tra questi PL/Java, PL/PHP e PL/Perl, mentre i data provider per .NET Npgsql e PgsqlClient sono stati migliorati per supportare i molti nuovi utenti sotto Windows.</blockquote><br /><br />Io sono di parte ma lo dico in ogni caso: ritengo PostgreSQL uno dei più bei "piece-of-software" mai partoriti dalla Comunity OS. Grazie.<div style="clear:both; padding-bottom: 0.25em;"></div>
#!/bin/bash
for x in 'AC-DC' 'Aerosmith' 'Anthrax' 'Barry White' 'Big Bad Voodoo Daddy' 'Bloodywood' 'Bobby Darin' 'Bob Marley' 'Bob Marley & the Wailers' 'Caparezza' 'Cypress Hill' 'Dean Martin' 'Dynamite Hack' 'Elvis Presley' 'Eminem' 'Faith No More' 'Frank Sinatra' 'George Clinton' 'Gorillaz' "Guns N' Roses" 'Jimmy Buffett' 'Joe Pesci' 'Johann Sebastian Bach' 'Judgment Night' 'Kaleido' 'Korn' 'Led Zeppelin' 'Lenny Kravitz' 'Leo Moracchioli' 'Levellers' 'Limp Bizkit' 'Linkin Park' 'Living Colour' 'Lou Monte' 'Luciano Pavarotti' 'Mondo Cane' 'Michael Bublé' 'Mr. Bungle' 'Peeping Tom' 'Poison' 'Prince' 'Queen' 'Red Hot Chili Peppers' 'Richard Cheese' 'Scatterbrain' 'Shaggy' 'Skid Row' 'Steve Tyrell' 'System Of A Down' 'The Levellers' 'The Rolling Stones' 'Tomahawk' 'Tom Jones' 'Tony Bennett' 'Tool' 'Van Halen' 'Weird Al Yankovic' 'Andrea Bocelli' 'Snarky Puppy' 'In.Si.Dia' 'Fortunate Youth' 'Alborosie' 'Skindred' 'Dolphin Traders' 'Fear Nuttin Band' 'Stick Figure' 'Tribal Seeds' 'Africa Unite' 'Hirie' 'Vitamin String Quartet' 'Ultraphonix' 'John Zorn' 'Prophets Of Rage' 'Drowning Pool' 'Kid Rock' 'They Might Be Giants' 'Sausage' 'Otep' 'Marracash' 'Lacuna Coil' 'Seth MacFarlane' 'Primus' 'Jonathan Davis' 'Disturbed' 'Mike Patton' 'Body Count' 'Quartiere Coffee' 'Zucchero'; do

  ln -s "/mnt/gluster/media/music/$x"

done


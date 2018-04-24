/**
 *Tía Agatha, el carnicero y Charles son las únicas personas que viven en la mansión Dreadbury. 
 */
viveEnLaMansion(agatha).
viveEnLaMansion(carnicero).
viveEnLaMansion(charles).
%Reglas
/* Agatha odia a todos los que viven en la mansión, excepto al carnicero. */
odiaA(agatha,Persona):-
  viveEnLaMansion(Persona),
  not(Persona=carnicero).
/* Charles odia a todas las personas de la mansión que no son odiadas por la tía Agatha.*/
odiaA(charles,Persona):-
  viveEnLaMansion(Persona),
  not(odiaA(agatha,Persona)).
/* El carnicero odia a las mismas personas que odia tía Agatha. */
odiaA(carnicero,Persona):-odiaA(agatha,Persona).
/* Quien no es odiado por el carnicero y vive en la mansión, es más rico que tía Agatha */
esMasRicoQue(Persona,agatha):-
  viveEnLaMansion(Persona),
  not(odiaA(carnicero,Persona)).
/* Un asesino siempre odia a su víctima y nunca es más rico que ella. El asesino de la tía
Agatha, además, vive en la mansión Dreadbury.*/
esAsesinoDe(Asesino,Victima):-
  viveEnLaMansion(Asesino),
  not(esMasRicoQue(Asesino,Victima)),
  odiaA(Asesino,Victima).

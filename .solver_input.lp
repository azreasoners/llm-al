#base.

% -------------------------------------------------------------------------
% preamble ----------------------------------------------------------------
% -------------------------------------------------------------------------


% -------------------------------------------------------------------------
% main body ---------------------------------------------------------------
% -------------------------------------------------------------------------

#const maxAdditive=6.


% Sort Declarations ---------------------------------------------------

#hide s_vessel/1.
#hide s_location/1.
#hide s_group/1.
#hide s_integer/1.

% ---------------------------------------------------------------------



% Object Declarations -------------------------------------------------

s_vessel(o_boat) :- true.
s_location(o_bank1) :- true.
s_location(o_bank2) :- true.
s_group(o_missionaries) :- true.
s_group(o_cannibals) :- true.
s_group(o_jesus) :- true.
s_integer(0..10).

% ---------------------------------------------------------------------



% Variable Declarations -----------------------------------------------

#domain s_vessel(V_Vessel).
#domain s_group(V_G).
#domain s_location(V_Loc).
#domain s_integer(V_N).
#domain s_integer(V_N1).
#domain s_integer(V_N2).
#domain s_integer(V_Cap).
#domain s_integer(V_N_m).
#domain s_integer(V_N_c).
#domain s_integer(V_L_m).
#domain s_integer(V_L_c).
#domain s_integer(V_Rem_m).
#domain s_integer(V_Rem_c).
#domain s_integer(V_T).
s_boolean(o_true) :- true.
s_boolean(o_false) :- true.
#hide s_boolean/1.
#domain s_boolean(V_Bool).

% ---------------------------------------------------------------------



% Constant Declarations -----------------------------------------------

s_afValue(-maxAdditive..maxAdditive).
#hide s_afValue/1.
s_afValue(-maxAdditive..maxAdditive).
#domain s_group(GVAR_group_1).
#domain s_location(GVAR_location_1).
#domain s_group(GVAR_group_2).
#domain s_location(GVAR_location_2).
 :- not 1{c_f_2_numOnBank(GVAR_group_2,GVAR_location_2,LVAR_afValue_1,0):s_afValue(LVAR_afValue_1)}1.
#cumulative t.
 :- not 1{c_f_2_numOnBank(GVAR_group_1,GVAR_location_1,LVAR_afValue_1,t):s_afValue(LVAR_afValue_1)}1.
#hide contrib_numOnBank/4.
{contrib_numOnBank(GVAR_group_1,GVAR_location_1,ACTION,0,t-1)} :- additiveconst_action(c_f_2_numOnBank(GVAR_group_1,GVAR_location_1),ACTION).
 :- not 1{contrib_numOnBank(GVAR_group_1,GVAR_location_1,ACTION,VAR,t-1):s_afValue(VAR)}1,additiveconst_action(c_f_2_numOnBank(GVAR_group_1,GVAR_location_1),ACTION).
c_f_2_numOnBank(GVAR_group_1,GVAR_location_1,VAR1+VAR2,t) :- VAR1=#sum[contrib_numOnBank(GVAR_group_1,GVAR_location_1,ACTION,VAR3,t-1):additiveconst_action(c_f_2_numOnBank(GVAR_group_1,GVAR_location_1),ACTION):s_afValue(VAR3)=VAR3],c_f_2_numOnBank(GVAR_group_1,GVAR_location_1,VAR2,t-1).
#domain s_afValue(GVAR_afValue_1).
#base.
{c_f_2_numOnBank(GVAR_group_1,GVAR_location_1,GVAR_afValue_1,0)} :- true.
 :- c_f_2_numOnBank(GVAR_group_1,GVAR_location_1,VAR,0),not s_afValue(VAR).
#cumulative t.
 :- c_f_2_numOnBank(GVAR_group_1,GVAR_location_1,VAR,t),not s_afValue(VAR).
#base.
 :- not 1{c_f_0_jesusLocation(LVAR_location_1,0):s_location(LVAR_location_1)}1.
#cumulative t.
 :- not 1{c_f_0_jesusLocation(LVAR_location_1,t):s_location(LVAR_location_1)}1.
{c_f_0_jesusLocation(GVAR_location_1,t)} :- c_f_0_jesusLocation(GVAR_location_1,t-1).
#base.
{c_f_0_jesusLocation(GVAR_location_1,0)} :- true.
 :- c_f_0_jesusLocation(VAR,0),not s_location(VAR).
#cumulative t.
 :- c_f_0_jesusLocation(VAR,t),not s_location(VAR).
#base.
 :- not 1{c_f_0_boatLocation(LVAR_location_1,0):s_location(LVAR_location_1)}1.
#cumulative t.
 :- not 1{c_f_0_boatLocation(LVAR_location_1,t):s_location(LVAR_location_1)}1.
{c_f_0_boatLocation(GVAR_location_1,t)} :- c_f_0_boatLocation(GVAR_location_1,t-1).
#base.
{c_f_0_boatLocation(GVAR_location_1,0)} :- true.
 :- c_f_0_boatLocation(VAR,0),not s_location(VAR).
#cumulative t.
 :- c_f_0_boatLocation(VAR,t),not s_location(VAR).
#base.
s_boolean__none(VAR) :- s_boolean(VAR).
s_boolean__none(o_true) :- true.
s_boolean__none(o_false) :- true.
s_boolean__none(o_none) :- true.
#hide s_boolean__none/1.
#domain s_vessel(GVAR_vessel_1).
#domain s_vessel(GVAR_vessel_2).
#cumulative t.
 :- not 1{c_a_1_cross(GVAR_vessel_2,LVAR_boolean_1,t-1):s_boolean(LVAR_boolean_1)}1.
#domain s_boolean(GVAR_boolean_1).
{c_a_1_cross(GVAR_vessel_1,GVAR_boolean_1,t-1)} :- true.
 :- c_a_1_cross(GVAR_vessel_1,VAR,t-1),not s_boolean(VAR).
#base.
s_integer__none(o_none) :- true.
s_integer__none(0..10).
#hide s_integer__none/1.
s_integer__none(VAR) :- s_integer(VAR).
#cumulative t.
 :- not 1{c_a_2_loading(GVAR_vessel_2,GVAR_group_2,LVAR_integer__none_1,t-1):s_integer__none(LVAR_integer__none_1)}1.
 :- 1{c_a_2_loading(GVAR_vessel_1,GVAR_group_1,o_none,t-1),c_a_1_cross(GVAR_vessel_1,o_false,t-1)}1.
#domain s_integer__none(GVAR_integer__none_1).
{c_a_2_loading(GVAR_vessel_1,GVAR_group_1,GVAR_integer__none_1,t-1)} :- true.
 :- c_a_2_loading(GVAR_vessel_1,GVAR_group_1,VAR,t-1),not s_integer__none(VAR).
 :- not 1{c_a_1_jesusOnBoat(GVAR_vessel_2,LVAR_boolean__none_1,t-1):s_boolean__none(LVAR_boolean__none_1)}1.
 :- 1{c_a_1_jesusOnBoat(GVAR_vessel_1,o_none,t-1),c_a_1_cross(GVAR_vessel_1,o_false,t-1)}1.
#domain s_boolean__none(GVAR_boolean__none_1).
{c_a_1_jesusOnBoat(GVAR_vessel_1,GVAR_boolean__none_1,t-1)} :- true.
 :- c_a_1_jesusOnBoat(GVAR_vessel_1,VAR,t-1),not s_boolean__none(VAR).
 :- not 1{c_a_0_walk(LVAR_boolean_1,t-1):s_boolean(LVAR_boolean_1)}1.
{c_a_0_walk(GVAR_boolean_1,t-1)} :- true.
 :- c_a_0_walk(VAR,t-1),not s_boolean(VAR).
#base.
 :- not 1{c_f_1_capacity(GVAR_vessel_2,LVAR_integer_1,0):s_integer(LVAR_integer_1)}1.
#cumulative t.
 :- not 1{c_f_1_capacity(GVAR_vessel_1,LVAR_integer_1,t):s_integer(LVAR_integer_1)}1.
#domain s_integer(GVAR_integer_1).
{c_f_1_capacity(GVAR_vessel_1,GVAR_integer_1,t)} :- c_f_1_capacity(GVAR_vessel_1,GVAR_integer_1,t-1).
#base.
{c_f_1_capacity(GVAR_vessel_1,GVAR_integer_1,0)} :- true.
 :- c_f_1_capacity(GVAR_vessel_1,VAR,0),not s_integer(VAR).
#cumulative t.
 :- c_f_1_capacity(GVAR_vessel_1,VAR,t),not s_integer(VAR).
#base.
 :- not 1{c_f_1_totalNum(GVAR_group_2,LVAR_integer_1,0):s_integer(LVAR_integer_1)}1.
#cumulative t.
 :- not 1{c_f_1_totalNum(GVAR_group_1,LVAR_integer_1,t):s_integer(LVAR_integer_1)}1.
{c_f_1_totalNum(GVAR_group_1,GVAR_integer_1,t)} :- c_f_1_totalNum(GVAR_group_1,GVAR_integer_1,t-1).
#base.
{c_f_1_totalNum(GVAR_group_1,GVAR_integer_1,0)} :- true.
 :- c_f_1_totalNum(GVAR_group_1,VAR,0),not s_integer(VAR).
#cumulative t.
 :- c_f_1_totalNum(GVAR_group_1,VAR,t),not s_integer(VAR).
#base.

% ---------------------------------------------------------------------


% Generated constraints
% 1a Crossing the boat causes the boatLocation to change from bank1 to bank2

#cumulative t.
c_f_0_boatLocation(o_bank2,t) :- c_a_1_cross(V_Vessel,o_true,t-1),c_f_0_boatLocation(o_bank1,t-1).

% 1b Crossing the boat causes the boatLocation to change from bank2 to bank1

c_f_0_boatLocation(o_bank1,t) :- c_a_1_cross(V_Vessel,o_true,t-1),c_f_0_boatLocation(o_bank2,t-1).

% 2 Crossing the boat causes numOnBank(group, boatLocation) to decrease by loading(Vessel, group) for each group

#base.
additiveconst_action(c_f_2_numOnBank(V_G,GVAR_location_1),c_a_1_cross(V_Vessel)) :- c_f_0_boatLocation(GVAR_location_1,0).

#cumulative t.
contrib_numOnBank(V_G,GVAR_location_2,c_a_1_cross(V_Vessel),-(V_N),t-1) :- c_a_1_cross(V_Vessel,o_true,t-1),c_f_0_boatLocation(GVAR_location_2,t-1),c_a_2_loading(V_Vessel,V_G,V_N,t-1).

% 3a Crossing the boat from bank1 to bank2 increases numOnBank(G, bank2) by loading(Vessel, G)

#base.
additiveconst_action(c_f_2_numOnBank(V_G,o_bank2),c_a_1_cross(V_Vessel)) :- true.

#cumulative t.
contrib_numOnBank(V_G,o_bank2,c_a_1_cross(V_Vessel),V_N,t-1) :- c_a_1_cross(V_Vessel,o_true,t-1),c_f_0_boatLocation(o_bank1,t-1),c_a_2_loading(V_Vessel,V_G,V_N,t-1).

% 3b Crossing the boat from bank2 to bank1 increases numOnBank(G, bank1) by loading(Vessel, G)

#base.
additiveconst_action(c_f_2_numOnBank(V_G,o_bank1),c_a_1_cross(V_Vessel)) :- true.

#cumulative t.
contrib_numOnBank(V_G,o_bank1,c_a_1_cross(V_Vessel),V_N,t-1) :- c_a_1_cross(V_Vessel,o_true,t-1),c_f_0_boatLocation(o_bank2,t-1),c_a_2_loading(V_Vessel,V_G,V_N,t-1).

% 4a Crossing the boat causes jesusLocation to change to bank2 if jesusOnBoat(Vessel) = true and boatLocation is bank1

c_f_0_jesusLocation(o_bank2,t) :- c_a_1_cross(V_Vessel,o_true,t-1),c_f_0_boatLocation(o_bank1,t-1),c_a_1_jesusOnBoat(V_Vessel,o_true,t-1).

% 4b Crossing the boat causes jesusLocation to change to bank1 if jesusOnBoat(Vessel) = true and boatLocation is bank2

c_f_0_jesusLocation(o_bank1,t) :- c_a_1_cross(V_Vessel,o_true,t-1),c_f_0_boatLocation(o_bank2,t-1),c_a_1_jesusOnBoat(V_Vessel,o_true,t-1).

% 5a Walking causes jesusLocation to change to bank2 if jesusLocation = bank1

c_f_0_jesusLocation(o_bank2,t) :- c_a_0_walk(o_true,t-1),c_f_0_jesusLocation(o_bank1,t-1).

% 5b Walking causes jesusLocation to change to bank1 if jesusLocation = bank2

c_f_0_jesusLocation(o_bank1,t) :- c_a_0_walk(o_true,t-1),c_f_0_jesusLocation(o_bank2,t-1).

% 6a Crossing the boat is not executable if jesusOnBoat(Vessel) = true and the total number of people loaded onto the boat (including Jesus) is less than one

 :- c_a_1_cross(V_Vessel,o_true,t-1),c_a_2_loading(V_Vessel,o_missionaries,V_N1,t-1),c_a_2_loading(V_Vessel,o_cannibals,V_N2,t-1),c_a_1_jesusOnBoat(V_Vessel,o_true,t-1),V_N1+V_N2+1<1.

% 6b Crossing the boat is not executable if jesusOnBoat(Vessel) = false and the total number of people loaded onto the boat is less than one

 :- c_a_1_cross(V_Vessel,o_true,t-1),c_a_2_loading(V_Vessel,o_missionaries,V_N1,t-1),c_a_2_loading(V_Vessel,o_cannibals,V_N2,t-1),c_a_1_jesusOnBoat(V_Vessel,o_false,t-1),V_N1+V_N2<1.

% 7a Crossing the boat is not executable if jesusOnBoat(Vessel) = true and the total number of people loaded onto the boat exceeds capacity(Vessel)

 :- c_a_1_cross(V_Vessel,o_true,t-1),c_a_2_loading(V_Vessel,o_missionaries,V_N1,t-1),c_a_2_loading(V_Vessel,o_cannibals,V_N2,t-1),c_f_1_capacity(V_Vessel,V_Cap,t-1),c_a_1_jesusOnBoat(V_Vessel,o_true,t-1),V_N1+V_N2+1>V_Cap.

% 7b Crossing the boat is not executable if jesusOnBoat(Vessel) = false and the total number of people loaded onto the boat exceeds capacity(Vessel)

 :- c_a_1_cross(V_Vessel,o_true,t-1),c_a_2_loading(V_Vessel,o_missionaries,V_N1,t-1),c_a_2_loading(V_Vessel,o_cannibals,V_N2,t-1),c_f_1_capacity(V_Vessel,V_Cap,t-1),c_a_1_jesusOnBoat(V_Vessel,o_false,t-1),V_N1+V_N2>V_Cap.

% 8 Crossing the boat is not executable if loading(Vessel, group) is greater than numOnBank(group, boatLocation) for any group

 :- c_a_1_cross(V_Vessel,o_true,t-1),c_a_2_loading(V_Vessel,V_G,V_N,t-1),c_f_2_numOnBank(V_G,GVAR_location_1,V_N1,t-1),V_N>V_N1,c_f_0_boatLocation(GVAR_location_1,t-1).

% 9a Crossing the boat is not executable if cannibals loaded onto the boat exceed missionaries loaded onto the boat plus one if jesusOnBoat(Vessel) = true

 :- c_a_1_cross(V_Vessel,o_true,t-1),c_a_2_loading(V_Vessel,o_cannibals,V_N_c,t-1),c_a_2_loading(V_Vessel,o_missionaries,V_N_m,t-1),c_a_1_jesusOnBoat(V_Vessel,o_true,t-1),V_N_c>V_N_m+1.

% 9b Crossing the boat is not executable if cannibals loaded onto the boat exceed missionaries loaded onto the boat if jesusOnBoat(Vessel) = false

 :- c_a_1_cross(V_Vessel,o_true,t-1),c_a_2_loading(V_Vessel,o_cannibals,V_N_c,t-1),c_a_2_loading(V_Vessel,o_missionaries,V_N_m,t-1),c_a_1_jesusOnBoat(V_Vessel,o_false,t-1),V_N_c>V_N_m.

% 10a Crossing the boat is not executable if cannibals remaining on the starting bank after loading would outnumber missionaries remaining on the starting bank plus one when Jesus is at that bank and not on the boat

 :- c_a_1_cross(V_Vessel,o_true,t-1),c_f_0_boatLocation(V_Loc,t-1),c_f_0_jesusLocation(V_Loc,t-1),c_a_1_jesusOnBoat(V_Vessel,o_false,t-1),c_f_2_numOnBank(o_cannibals,V_Loc,V_N_c,t-1),c_a_2_loading(V_Vessel,o_cannibals,V_L_c,t-1),V_Rem_c==V_N_c-V_L_c,c_f_2_numOnBank(o_missionaries,V_Loc,V_N_m,t-1),c_a_2_loading(V_Vessel,o_missionaries,V_L_m,t-1),V_Rem_m==V_N_m-V_L_m,V_Rem_c>V_Rem_m+1.

% 10b Crossing the boat is not executable if cannibals remaining on the starting bank after loading would outnumber missionaries remaining on the starting bank when Jesus is not at that bank

 :- c_a_1_cross(V_Vessel,o_true,t-1),c_f_0_boatLocation(V_Loc,t-1),GVAR_location_1!=V_Loc,c_f_2_numOnBank(o_cannibals,V_Loc,V_N_c,t-1),c_a_2_loading(V_Vessel,o_cannibals,V_L_c,t-1),V_Rem_c==V_N_c-V_L_c,c_f_2_numOnBank(o_missionaries,V_Loc,V_N_m,t-1),c_a_2_loading(V_Vessel,o_missionaries,V_L_m,t-1),V_Rem_m==V_N_m-V_L_m,V_Rem_c>V_Rem_m,c_f_0_jesusLocation(GVAR_location_1,t-1).

% 11a Walking is not executable if Jesus is already at bank2

 :- c_a_0_walk(o_true,t-1),c_f_0_jesusLocation(o_bank2,t-1).

% 11b Walking is not executable if Jesus is already at bank1

 :- c_a_0_walk(o_true,t-1),c_f_0_jesusLocation(o_bank1,t-1).

% 12a At any time, the total number of people in each group equals totalNum(group) if the group is not jesus

 :- V_G!=o_jesus,{not c_f_2_numOnBank(V_G,o_bank1,V_N1,t-1)}0,{not c_f_2_numOnBank(V_G,o_bank2,V_N2,t-1)}0,{not c_f_1_totalNum(V_G,V_T,t-1)}0,V_N1+V_N2!=V_T.

% 12b For Jesus individually

 :- {not c_f_0_jesusLocation(V_Loc,t-1)}0,not c_f_2_numOnBank(o_jesus,V_Loc,1,t-1).

#domain s_location(_NV_1).
 :- _NV_1!=V_Loc,{not c_f_0_jesusLocation(_NV_1,t-1)}0,not c_f_2_numOnBank(o_jesus,V_Loc,0,t-1).

% 14a It is impossible for cannibals to outnumber missionaries on any bank when Jesus is at that bank

#base.
 :- V_N_c>V_N_m+1,c_f_2_numOnBank(o_cannibals,V_Loc,V_N_c,0),c_f_2_numOnBank(o_missionaries,V_Loc,V_N_m,0),c_f_0_jesusLocation(V_Loc,0).
#cumulative t.
 :- V_N_c>V_N_m+1,c_f_2_numOnBank(o_cannibals,V_Loc,V_N_c,t),c_f_2_numOnBank(o_missionaries,V_Loc,V_N_m,t),c_f_0_jesusLocation(V_Loc,t).

% 14b It is impossible for cannibals to outnumber missionaries on any bank when Jesus is not at that bank

#base.
 :- V_N_c>V_N_m,c_f_2_numOnBank(o_cannibals,V_Loc,V_N_c,0),c_f_2_numOnBank(o_missionaries,V_Loc,V_N_m,0),GVAR_location_1!=V_Loc,c_f_0_jesusLocation(GVAR_location_1,0).
#cumulative t.
 :- V_N_c>V_N_m,c_f_2_numOnBank(o_cannibals,V_Loc,V_N_c,t),c_f_2_numOnBank(o_missionaries,V_Loc,V_N_m,t),GVAR_location_2!=V_Loc,c_f_0_jesusLocation(GVAR_location_2,t).

% 15a It is not permissible for cannibals to outnumber missionaries on the boat during crossing when Jesus is on the boat

 :- c_a_1_cross(V_Vessel,o_true,t-1),c_a_2_loading(V_Vessel,o_cannibals,V_N_c,t-1),c_a_2_loading(V_Vessel,o_missionaries,V_N_m,t-1),c_a_1_jesusOnBoat(V_Vessel,o_true,t-1),V_N_c>V_N_m+1.

% 15b It is not permissible for cannibals to outnumber missionaries on the boat during crossing when Jesus is not on the boat

 :- c_a_1_cross(V_Vessel,o_true,t-1),c_a_2_loading(V_Vessel,o_cannibals,V_N_c,t-1),c_a_2_loading(V_Vessel,o_missionaries,V_N_m,t-1),c_a_1_jesusOnBoat(V_Vessel,o_false,t-1),V_N_c>V_N_m.

% 17 Loading(Vessel, group) during a crossing must be at least zero (cannot be negative)

 :- c_a_1_cross(V_Vessel,o_true,t-1),c_a_2_loading(V_Vessel,V_G,V_N,t-1),V_N<0.

% 19 It is not permissible to cross the boat and walk at the same time

 :- c_a_1_cross(V_Vessel,o_true,t-1),c_a_0_walk(o_true,t-1),true.

% 20 The capacity of the boat is 2

#base.
c_f_1_capacity(o_boat,2,0) :- true.
#cumulative t.
c_f_1_capacity(o_boat,2,t) :- true.

% Total number of people in each group

#base.
c_f_1_totalNum(o_missionaries,3,0) :- true.
#cumulative t.
c_f_1_totalNum(o_missionaries,3,t) :- true.

#base.
c_f_1_totalNum(o_cannibals,3,0) :- true.
#cumulative t.
c_f_1_totalNum(o_cannibals,3,t) :- true.

#base.
c_f_1_totalNum(o_jesus,1,0) :- true.
#cumulative t.
c_f_1_totalNum(o_jesus,1,t) :- true.

% Initial conditions (if not already specified elsewhere)

#base.
c_f_0_boatLocation(o_bank1,0) :- true.
#cumulative t.
c_f_0_boatLocation(o_bank1,t) :- true.

#base.
c_f_0_jesusLocation(o_bank1,0) :- true.
#cumulative t.
c_f_0_jesusLocation(o_bank1,t) :- true.

% noconcurrency

% Query: 0
% Maxstep: 
#base.
 :- not c_f_2_numOnBank(o_missionaries,o_bank1,3,0),query_label(q_0).
 :- not c_f_2_numOnBank(o_cannibals,o_bank1,3,0),query_label(q_0).
 :- not c_f_2_numOnBank(o_missionaries,o_bank2,0,0),query_label(q_0).
 :- not c_f_2_numOnBank(o_cannibals,o_bank2,0,0),query_label(q_0).
 :- not c_f_0_jesusLocation(o_bank1,0),query_label(q_0).
 :- not c_f_0_boatLocation(o_bank1,0),query_label(q_0).
 :- not c_f_2_numOnBank(o_missionaries,o_bank2,3,0),maxstep==0,query_label(q_0).
 :- not c_f_2_numOnBank(o_cannibals,o_bank2,3,0),maxstep==0,query_label(q_0).
 :- not c_f_2_numOnBank(o_missionaries,o_bank1,0,0),maxstep==0,query_label(q_0).
 :- not c_f_2_numOnBank(o_cannibals,o_bank1,0,0),maxstep==0,query_label(q_0).
 :- not c_f_0_jesusLocation(o_bank2,0),maxstep==0,query_label(q_0).
#volatile t.
 :- not c_f_2_numOnBank(o_missionaries,o_bank2,3,t),query_label(q_0).
 :- not c_f_2_numOnBank(o_cannibals,o_bank2,3,t),query_label(q_0).
 :- not c_f_2_numOnBank(o_missionaries,o_bank1,0,t),query_label(q_0).
 :- not c_f_2_numOnBank(o_cannibals,o_bank1,0,t),query_label(q_0).
 :- not c_f_0_jesusLocation(o_bank2,t),query_label(q_0).


% -------------------------------------------------------------------------
% noconcurrency -----------------------------------------------------------
% -------------------------------------------------------------------------

#cumulative t.
 :- c_a_1_cross(GVAR_vessel_1,o_true,t-1),c_a_1_cross(GVAR_vessel_2,o_true,t-1),GVAR_vessel_1!=GVAR_vessel_2.
 :- c_a_1_cross(GVAR_vessel_1,o_true,t-1),c_a_0_walk(o_true,t-1).
#base.

% -------------------------------------------------------------------------
% epilogue ----------------------------------------------------------------
% -------------------------------------------------------------------------

query_label(query) :- true.
#volatile t.
 :- t<minstep.
% -------------------------------------------------------------------------

#hide additiveconst_action/1.
#hide s_computed/1.
#hide query_label/1.
#base.
true.
:- false.
#hide true/0.

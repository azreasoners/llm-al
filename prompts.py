bc_description = '''Action language BC+ consists of (1) a signature, which is a finite set of propositional atoms, and (2) causal laws. An atom is true, false, or of the form c=v, where c is a constant, and v is an element in its domain. Constants c are divided into two groups: fluent constants and action constants. A formula is a propositional combination of atoms. A fluent formula is a formula such that all constants occurring in it are fluent constants. An action formula is a formula that contains at least one action constant and no fluent constants. 

For example, a fluent constant "loc" which represents the location of some object, may have a value from {l1, l2, l3}. To express the location is l2, one would write:
loc = l2.

Similarly, an action constant "drive" representing driving a car, may have a value from {true, false} (though in general actions can be non-boolean). To represent this, one could write:
drive = true.

For boolean constants c, c is shorthand for c=true, and ~c is shorthand for c=false. Thus "drive = true" can be represented simply as "drive". The standard logical operators are: "-" for negation, "&" for conjunction, "|" for disjunction, and "->" for implication.

Numeric values may combine with unary operators "-" (negative), "abs" (absolute value, e.g., abs(n)), and binary operators "+" (addition), "-" (subtraction), "*" (multiplication), "//" (floor division), and "mod" (modulus, e.g., n mod m). Comparison is done with "=" (equality), "\=" (inequality), "<" (less than), ">" (greater than), "<=" (less than or equal), and ">=" (greater than or equal).

An action description D is a set of causal laws that define a transition system, which can be represented as a directed graph. In this graph, the vertices correspond to states of the world, while the edges signify transitions between these states.

[CAUSAL LAWS: BASIC FORM]

In BC+, there are three types of basic laws: (1) static law, (2) action dynamic law, and (3) fluent dynamic law:

STATIC LAW:

	F if G,

where F and G are fluent formulas. This expresses that F is true if the formula G is true.

ACTION DYNAMIC LAW:

	F if G,

where F is an action formula and G is a formula. This expresses that action formula F is true if G is true.

FLUENT DYNAMIC LAW:

	F if G after H,

where F and G are fluent formulas, and H is a formula. This expresses that F is true if G is true after H is true.

[CAUSAL LAWS: SOME SHORTHAND ABBREVIATIONS]

BC+ allows several kinds of shorthand notation for the basic causal laws. These make it convenient to directly express commonsense knowledge.


CAUSES:

	a causes F if H,

where a is an action, F is a fluent formula, H is a formula, is shorthand for the fluent dynamic law:

	F after a & H.

This rule intuitively expresses that an action a causes some effect F if condition H is true.

IMPOSSIBLE:

	impossible F,

where F is a fluent formula, is shorthand for the static law:

	false if F.

This rule intuitively expresses that formula F should be false in every state.

NONEXECUTABLE:

	nonexecutable a_1 & ... & a_k if G,

where a_1 & ... & a_k are action constants and G is a formula, is shorthand for the fluent dynamic law:

	false if true after a_1 & ... & a_k & G.

This rule intuitively expresses that actions a_1 & ... & a_k all being true is not possible if G is true.

DEFAULT:

	default c=v if F,

where F is a fluent formula, stands for a static causal law. 

This intuitively expresses that by default c=v holds when F is true in the state. If there is evidence to the contrary, then c=v may not hold. 

	default c=v if F after G,

where F is a fluent formula, and G is a formula, and stands for a fluent dynamic law which intuitively expresses that by default c=v holds when F is true in the state and F was true in the previous state. If there is evidence to the contrary, then c=v may not hold.

ALWAYS:

	always F,

where F is a formula which can contain both fluent and action constants, is shorthand for the fluent dynamic law:

	false if true after ~F.

This rule intuitively expresses that every transition must satisfy F.

[SORT/OBJECT/VARIABLE/CONSTANT DECLARATION IMPLEMENTATION]

Action language BC+ is implemented in a program as follows. A BC+ program consists of a sort declaration, object declaration, variable declaration, constant declaration, along with a set of causal laws.

SORT DECLARATION:
A sort is a named set of elements which is used to specify the domain of each constant and variable. First the sort is declared
using a sort declaration statement and, later, is defined by adding objects to it in an object declaration statement.

Example:
:- sorts
    int;
    box.

This declares the sorts: int, and box.

A sort can also be a supersort, that is, a sort s can automatically include the objects within another sort s2, denoted s >> s2.

:- sorts
    package >> box.
This declares the sort package and box, where package is a supersort and includes the sort box.

OBJECT DECLARATION:
An object is a value in a sort which a constant can take. It is also used
in parameter lists to construct nested objects and sets of constants. 

Example:
:- objects
    1..3 :: int;
    o(int, int) :: box.

This declares 1,2, and 3 as objects within int, and the objects:
o(1, 1), o(1, 2), o(1, 3),
o(2, 1), o(2, 2), o(2, 3),
o(3, 1), o(3, 2), and o(3, 3),
as values within box.

Consider the following sort and object declaration:

:- sorts
    package >> box.

:- objects
    p1, p2 :: package;
    b1, b2, b3 :: box.

Since package is a supersort of box, there are 5 objects that are of sort package: p1, p2, b1, b2, and b3. There are only 3 objects of sort box: b1, b2 and b3.

VARIABLE DECLARATION:
A variable is a placeholder symbol which will be replaced with each object in its domain during grounding.

Example:
:- variables
    I, I1, I2 :: int;
    B, B1, B2 :: box.
This declares the variables I, I1, and I2 over the objects within int, and variables B, B1, and B2 range over the objects within box.
Variables are denoted as capital letters which are replaced with all possible values in the domain of their associated sort in a process called grounding.

CONSTANT DECLARATION:
Similar to object symbols, constants are defined within a constant declaration statement and have a base identifier, an optional list of parameter sort, and a sort which makes up the constant's domain. In addition, they have a constant declaration type, such as "exogenousAction" or "inertialFluent". Inertial fluents are common, and used for constants whose value persists through time unless affected otherwise.

Example:
:- constants
    p(int) :: inertialFluent(boolean);
    move(box) :: exogenousAction.
This declares the inertial fluent p which takes an int argument and is a boolean value, and the action move, which takes a box argument.

[CAUSAL LAWS BASIC FORM IMPLEMENTATION]

STATIC LAW EXAMPLE:

	F if G,

where F and G are fluent formulas, is written for example:

% The location of a person is the same as the car if the person is in the car.
loc(person)=L if inCar & loc(car)=L.

ACTION DYNAMIC LAW EXAMPLE:

	F if G,

where F is an action formula and G is a formula, is written for example:

% If A is assigned to location Loc, and it is ready, then moveTo(A) is true.
moveTo(A) if assigned(A) = Loc & ready(A),
where moveTo(A) is an action, and assigned(A) and ready(A) are fluent constants. Here moveTo is a boolean action constant.

FLUENT DYNAMIC LAW EXAMPLE:

	F if G after H,

where F and G are fluent formulas, and H is a formula, is written for example:

% If you enter the car after the car is unlocked, then you are in the car.
in(car) if unlocked(car) after enter(car).

[CAUSAL LAW SHORTHAND ABBREVIATIONS IMPLEMENTATION]

CAUSES EXAMPLE:

An expression of the form
	a causes F if H,

where a is an action, F is a fluent formula, H is a formula, is written for example:
% Driving the car to a location causes the car to be at that location of the car has gas.
drive(car, loc) causes location(car) = loc if hasGas(car)

IMPOSSIBLE EXAMPLE:

An expression of the form

	impossible F,

where F is a fluent formula, is written for example:

% The cat and mouse cannot be at the same location
impossible loc(cat)=Loc1 & loc(mouse) = Loc2 & Loc1=Loc2.

Recall that F in "impossible F" must be a fluent formula, meaning that F cannot contain action constants, including attributes.

The following two examples are incorrect, where drive(car) is an action, and numPassengers(car) and numDrivers(car) are attributes:
% The car cannot be driven if it has no fuel.
impossible drive(car) & fuel(car) = 0.

% The combined number of passengers and drivers cannot exceed 5.
impossible N1 + N2 > 5 & N1 = numPassengers(car) & N2 = numDrivers(car).

These are wrong because drive(car) is an action constant, and the attributes numPassengers and numDrivers are action constants, and they are in an impossible constraint.

NONEXECUTABLE EXAMPLE:

An expression of the form:

	nonexecutable a1 & a2 & ... & an if G, 

where a_1 & ... & a_k are action constants and G is a formula, is written for example:

% It is not permissible to drive a bus and a car if they are driving to the same location. 
nonexecutable driveCar(Loc1) & driveBus(Loc2) if Loc1=Loc2.

% It is not permissible to lift an object if it is heavy.
nonexecutable lift(object) if heavy(object).

On the other hand, the following:

nonexecutable lifted(object) if heavy(object),

is not allowed when lifted(object) is a fluent and not an action.

DEFAULT EXAMPLES:

An expression of the form

	default c=v if F,

where F is a fluent formula, is written for example as:

% By default, the power is on if the switch is turned.
default powerOn if switchTurned.

An expression of the form

	default c=v if F after G,

where F is a fluent formula, and G is a formula, is written for example as:

% The ferry will be on the right bank if it has gas after it was on the left bank, and no evidence suggests otherwise.
default ferry(right) if hasGas after ferry(left)

ALWAYS EXAMPLE:

	always F,

where F is a formula which can contain both fluent and action constants, is written for example:

% the number departing from a location is always less than or equal to the number at the location
always departing(Loc) <= numAt(Loc).

where departing/1 is an action constant and numAt/1 is a fluent.
Note: There should not be an "if" in a "always" rule, instead use "&".

Keep in mind that "always F" should be used for conditions which should be true for every transition.

[EXTENDED CONSTANT DECLARATION]
We can expand constant declaration to allow for attributes, additive fluents and additive actions.

ATTRIBUTES:
Attributes are types of action constants which are tied to actions, and given additional information about an action. For instance:

:- constants
    move(block) :: exogenousAction;
    destination(block) :: attribute(location) of move(block).

This declaration tells us that destination(block) is an attribute of the action of moving a block, which has value of location, representing the block's destination.

Important: Attributes should have as their first arguments, the same arguments (and in the same order) as the action which they are an attribute of.
For example, any attribute of the action "fly(airplane,location)" should have the form "attributeName(airplane,location,...)", after which the action arguments "airplane" and "location", can other arguments be listed.
An attribute which represents the number of passengers on board of a nationality can be written as:
onBoard(airplane,location,nationality) :: attribute(integer) of fly(airplane,location).

Where the following would be incorrect:
Incorrect: passengers(nationality) :: attribute(integer) of fly(airplane,location),
since passengers should instead have the arguments "airplane" and "location" before "nationality".

Important: If an attribute is ever declared, then the action it is an attribute of must have at least one argument.

For example, the above declaration would be incorrect if it was the following:

:- constants
    move :: exogenousAction;
    destination :: attribute(location) of move.

Here, since destination is an attribute of move, but move has no argument, this is wrong.

ADDITIVE FLUENTS AND ADDITIVE ACTIONS:

There are special constants additive fluents and additive actions, which are useful for modeling the effects of concurrent actions.
An additive fluent is a fluent (tied to states) with numerical values such that the effect of several concurrently executed actions on it can be computed by adding the effects of the individual actions.
An additive action constant (tied to a transition) is similar except that it can handle numeric values of concurrent actions during transitions.

With a buy and sell action, and numExchanged attribute of exchange, additive fluents and additive actions can be declared as follows:
:- constants
    buy(item) :: exogenousAction;
    sell(item) :: exogenousAction;
    exchange(item) :: exogenousAction;
    numExchanged(item) :: attribute(integer) of exchange(item); 
    inStock(item) :: additiveFluent(integer);
    netChange(item) :: additiveAction(integer).

inStock(item) represents the the number of an item in stock, which can be affected by both buy(item) and sell(item). netChange(item) represents the net number of an item which is exchanged or bought/sold during a given transition or event.

[EXTENDED CAUSAL LAW SHORTHAND ABBREVIATIONS: INCREMENT/DECREMENT LAWS IMPLEMENTATION]

INCREMENT/DECREMENT LAWS:
Additive fluents can only be updated in increment/decrement laws, which are expressed as:

    a increments c by v if G,

where a is an action, c is an additive fluent, v is an integer, and G is a fluent, is used to express that some additive fluent (c), should increase by some value v if G is true and action a happens.

Similarly:

    a decrements c by v if G,

is used to decrease the additive constant c by value v if G is true and action a happens.

Examples:
% buy(coin) increments has(coin) by N if howMany(coin,N).
% buy(coin) decrements has(money) by N*M if howMany(coin,N) & price(coin)=M.

Additive actions similarly are only updated in increment/decrement statements:

    a increments c by v if G.
    a decrements c by v if G.

where c is an additive action.
While additive fluents are used to describe state information, additive actions are about events/transitions. For example, suppose multiple actions can occur at once for a domain involving buying and selling, and the additive action netExchanged is declared:
% buy(coin) increments netExchanged(coin) by N if howMany(coin,N).
% sell(coin) decrements netExchanged(coin) by N if howMany(coin,N).

This is useful for tracking numerical values during a transition, which may be used, e.g., if there should never be a negative amount of net coins exchanged at a given time, then netExchanged(coin) can be used to construct such a law.

In general, if something causes something to increase/decrease, then we use increment/decrement. Updating the value of an additive fluent or action can only be done in an increment or decrement law (e.g., "a causes c=2" is not allowed if "c" represents an additive fluent/action).

[ARITHMETIC WITH ATTRIBUTES AND ADDITIVE CONSTANTS]
Attributes and additive actions should not occur in the operands of arithmetics such as addition, subtraction, multiplication, floor division, or modulus operators. They must be set to variables, and the variables must be used as the operands.

The following two rules are incorrect, where weight(truck,...) is an attribute:
% A truck cannot be driven if the combined weight of the cargo (C), passengers (P), and fuel (F), is greater than the truck's capacity.
nonexecutable drive(truck, P, C) if weight(truck, C) + weight(truck, P) + weight(truck, F) > capacity(truck).

% Driving the truck causes the weight of the truck's fuel to decrease by 15.
drive(truck, P, C) causes weight(truck, fuel) = weight(truck, fuel) - 15.

These are incorrect because the attributes weight(truck,...) are directly used in arithmetic.
Instead, these rules should be written as follows:
% A truck cannot be driven if the combined weight of the cargo (C), passengers (P), and fuel (F), is greater than the truck's capacity.
nonexecutable drive(truck, P, C) if N1 + N2 + N3 > capacity(truck) &  weight(truck, C) = N1 & weight(truck, P) = N2 & weight(truck, F) = N3.

% Driving the truck causes the weight of the truck's fuel to decrease by 15.
drive(truck, P, C) causes weight(truck, fuel) = N1 - 15 if N1 = weight(truck, fuel) & N2.

[RESTRICTION OF NESTED CONSTANTS]
A constant cannot appear as an argument of another constant. Instead, one can introduce a variable in place of a nested constant.

For example, the following is wrong since the (boolean) constant roadBlock(...), contains the nested constant loc(C):
nonexecutable move(C) if roadBlock(loc(C)).

Instead, loc(C) should be set to a variable, like the following:
nonexecutable move(C) if roadBlock(L) & L = loc(C).

[VARIABLE QUANTIFICATION]
When using "always F", make sure to quantify over variables if needed.
For example, say we want to express that the combined weight of passengers and the truck is less than the capacity of the truck. The following would be incorrect:
always weight(passengers) = N1 & weight(truck) = N2 & capacity(truck) = N3 & N1 + N2 < N3.

This is because of a quantification issue. This rule informally reads as "For all values N1, N2, and N3, the weight of the passengers is N1, the weight of the truck is N2, the capacity of the truck is N3, and N1 + N2 < N3." Since this will be grounded for every possible value that N1 can take it, there will be contradiction. Furthermore, the condition "N1 + N2 < N3" will obviously not hold over all possible values of the variables N1, N2, and N3.

To correctly write this, first set the variables in the antecedent of an implication:

always (weight(passengers) = N1 & weight(truck) = N2 & capacity(truck) = N3) -> N1 + N2 < N3.

This informally reads as "If the weight of the passengers is N1, the weight of the truck is N2, and the capacity of the truck is N3, then N1 + N2 < N3", and aligns with what we want to express.
'''


checklist = '''[CHECKLIST]
The following is a checklist which should be considered when writing and revising a BC+ program.
1. In general, if some conjunction of fluents cannot be true, then we use "impossible" when writing the rules, but if instead we want to assert some constant is caused to be false, then we use the negation (~). For example, if it is impossible for an object to be on the table and under it, we might write "impossible onTable(object) & underTable(object).", but express that no rain causes the ground to not be wet, we can write "~groundWet if noRain".
2. "impossible F" can only be used with fluents and "&". Do not use attributes or action constants in laws of the form "impossible F". "nonexecutable" is about actions not being permissible if certain fluents hold and/or certain actions are performed.
3. Additive constants can only be updated in increment/decrement laws.
4. In "a causes G if H", "G", recall G should be a fluent formula. Therefore, it should not directly contain action constants (including attributes). If one wants to set some constant to the value of an attribute, then the fluent formula G should contain a variable represnting the attribute, rather than the attribute itself.

For example, if the attribute nextDestination(Loc) is not set to a variable first, then this will be a malformed law error, since there is an action constant in G:
drive(car) causes loc(car) = nextDestination(Loc) if loc(boat) = Loc.

Instead, this should be written as:
drive(car) causes loc(car) = Loc2 if Loc2 = nextDestination(Loc) & loc(boat) = Loc.

This works because nextDestination(Loc) is first set to a variable.
5. Only use variables which are declared, if new variables are introduced, they must be declared.
6. In shorthand laws "default c=v if F" and "default c=v if F after G", "c" cannot be an additive constant, since this is can update the value of them, but they should only be updated in increment/decrement laws.
7. "always" shorthand abbreviations should not contain "if", but only conjunctions ("&").
8. In the case that a disjunction is used in the body of a rule, encapsulate it in parentheses, e.g., (loc(city1) | loc(city2)).
9. Do not nest constants in arguments of other constants. For example, do not use the following: nonexecutable move(C) if roadBlock(loc(C)). Instead, loc(C) should be set to a variable: nonexecutable move(C) if roadBlock(L) & L = loc(C).
10. Make sure that the query is exhaustive. For example, if the initial condition is that bus stop A has 10 people, and the goal condition is that the bus stop B has 10 people, it may need to be specified that bus stop B has 0 people in the initial condition, or the BC+ solver can just set the initial state to be the goal state.
11. Make sure to only use constants which are declared in the constant declaration. If new constans are used, then they must be added in the declaration.
12. Make sure when writing rules, that variables representing constants are of the correct sort, i.e., the sort of the variable is the same as the sort of the value of the constant it is representing.
For example, if there is a constant "capacity(vehicle)" which is of type "inertialFluent(integer)", then only variables of sort "integer" should be used to represent the constant in rules.
13. Don't use simple, or rigid fluents in the constant declaration. Use "inertialFluent" instead.
14. Don't use non-specified fluents. For example, there should not be constant declarations like "country(location) :: country", since this will be recognized as a rigid fluent.
15. Keep in mind that "always F" should be used for conditions which should be true for every transition and shout not be used to express conditions for a state. 

For example, consider a domain about trading coins that has the action constant numExchanged(coin), which is an attribute of some trading action, and the fluent constant amount(coin). numExchanged(coin) represents the net number of coins exchanged in a transition, from possibly multiple trade actions. amount(coin) represents the number of coins in a state (before and after trades).

If one wants to express that the net number of exchanged coins during an action is smaller than some limit for every trade, this can be expressed with:
always netExchanged(coin) < limit(coin).

However, if one wants to express that the amount of coins does not exceed some limit, this cannot be expressed with "always F". The following is incorrect:
always amount(coin) <= limit(coin).

This wrong because if a state does not have a transition to another state, then the condition "amount(coin) <= limit(coin)" can be false. For example, in a transition system with a single state, or the last state in a transition system.

Instead, it can be expressed as:
impossible amount(coint) > limit(coin).

This enforces the following is true for every state.
16. Attributes and additive actions should not occur in the operands of arithmetics such as addition, subtraction, multiplication, floor division, or modulus operators. They must be set to variables, and the variables must be used as the operands.'''




rule_gen = f'''{bc_description}

QUERIES:
Queries have three components: an optional label, an optional maximum step which list formulas which should be true in the last step of the plan, and a set of constraint formulas to apply, each parametrized with the step at which they should be applied.
For example the following query represents an initial state and an action at step 0, and a set of constraints which should be met at the end of the plan.

:- query
	label :: test_query;
	0: loc(b1)=b2 & loc(b2)=b3 & loc(b3)=a & loc(b4)=b & loc(b5)=c;
	0: move(b1, b5);
	maxstep: loc(b5,c) & loc(b4,b5) & loc(b3,b4) & loc(b2,b3) & loc(b1,b2).

Here are some example Programs.

[EXAMPLE 1]

Problem description:
Blocks can be stacked on top of each other or on a table. Blocks stacked on the table are in a tower.

There are two main types of things: loc and block.
loc includes block.

b1, b2, b3, and b4 are blocks.
table is a loc.

Actions
Moving a block to a location.

Query (in natural language):
Initially, block b1 is on b2, b2 is on the table, b3 is on the table, and b4 is on b3. Find a plan so that block b1 is on b4, b2 is on b3, b3 is on b1, and b4 is on the table.

BC+ Program:
:- sorts
    loc >> block.
:- objects
    b1, b2, b3, b4 :: block;
    table :: loc.
:- constants
    loc(block) :: inertialFluent(loc);
    in_tower(block) :: inertialFluent(boolean);
    move(block, loc) :: exogenousAction.
:- variables
    B, B1, B2, B4 :: block;
    L, L1, L2, L3 :: loc.

% Two blocks cannot be at the same location. (Use loc(block). Since it is a fluent, we use impossible. Since we use impossible, we only use "&". "if" is not allowed). Use "\=" to differentiate B1 and B2.
impossible loc(B1) = B & loc(B2) = B & B1\=B2. 

% A block is in a tower if it's location is on the table. ("Static law")
in_tower(B) if loc(B) = table.

% A block is in a tower if it's location is on something that is in a tower. ("Static law")
in_tower(B) if loc(B) = B1 & in_tower(B1).

% Blocks don't float in the air. (Use in_tower(block). Since it is a fluent, we use impossible. Since we use impossible, we only use "&". "if" is not allowed)
impossible ~in_tower(B).

% Moving a block causes it's location to move to loc. ("causes" rule)
move(B,L) causes loc(B)=L.

% The move action is not permissible if something is on the location to be moved to. (Use move(block, loc). Since it is an action, we use nonexecutable.)
nonexecutable move(B,L) if loc(B1) = B.

% A block is in tower after it is in tower and it is on a block.
in_tower(B) after in_tower(B) and loc(B)=B1.

% By default, all blocks are in a tower.
default ~in_tower(B).

:- query
	0: loc(b1) = b2 & loc(b2) = table & loc(b3) = table & loc(b4)=b3);
	maxstep: loc(b1) = b4 & loc(b2) = b3 & loc(b3)=b1 & loc(b4) = table. 

[EXAMPLE 2]

Problem description:
A monkey wants to get a bunch of bananas hanging from the ceiling. He can reach the bananas by first pushing a box to the empty place under the bananas and then climbing on top of the box.

There are three main types of things: "monkey", "thing" and "location".
"thing" includes "monkey".

monkey, bananas, and box are things.
l1, l2, and l3 are locations.

Actions
walk to a location
push box to a location
climb on
climb off
grasp bananas

Query (in natural language):
Initially, the monkey is at location l1, the box is at l2, and the bananas are at location l3. Generate a plan so that the monkey has the bananas.

BC+ program:
:- sorts
    thing;
    location.

:- objects
    monkey,bananas,box :: thing;
    l1,l2,l3 :: location.

:- variables
    Loc, Loc1, Loc2 :: location;
    Bool, Bool1, Bool2 :: boolean.

:- constants
    loc(thing) :: inertialFluent(location);
    hasBananas,onBox :: inertialFluent;
    walk(location) :: exogenousAction;
    pushBox(location) :: exogenousAction;
    climbOn :: exogenousAction;
    climbOff :: exogenousAction;
    graspBananas :: exogenousAction.

% The location of the bananas is where the monkey is if the monkey has bananas.
loc(bananas)=Loc if hasBananas & loc(monkey)=Loc.

% The location of the monkey is where the box is if the monkey is on the box. 
loc(monkey)=Loc if onBox & loc(box)=Loc.

% The monkey cannot be in two places at once.
impossible loc(monkey) = Loc1 & loc(monkey)=Loc2 & Loc1\=Loc2.

% Walking to a location causes the monkey's location to change.
walk(Loc) causes loc(monkey)=Loc.

% Walking is not permissible to a location if the monkey is already in that location.
nonexecutable walk(Loc) if loc(monkey)=Loc.

% Walking is not permissible if the monkey is on the box.
nonexecutable walk(Loc) if onBox.

% Pushing the box to a location causes the location of the box to move.
pushBox(Loc) causes loc(box)=Loc.

% Pushing the box to a location causes the location of the monkey to move.
pushBox(Loc) causes loc(monkey)=Loc.

% Pushing the box is not permissible to a location if the monkey is at that location.
nonexecutable pushBox(Loc) if loc(monkey)=Loc.

% Pushing the box is not permissible if the monkey is on the box.
nonexecutable pushBox(Loc) if onBox.

% Pushing the box is not permissible if the location of the monkey is not the same as the location of the box.
nonexecutable pushBox(Loc) if loc(monkey)\=loc(box).

% Climbing on the box causes the monkey to be on the box.
climbOn causes onBox.

% Climbing on the box is not permissible if the monkey is already on the box.
nonexecutable climbOn if onBox.

% Climbing on the box is not permissible if the location of the monkey is not the same as the box.
nonexecutable climbOn if loc(monkey)\=loc(box).

% Climbing off of the box causes the monkey to not be on the box.
climbOff causes ~onBox.

% Climbing off of the box is not permissible if the monkey is not on the box.
nonexecutable climbOff if ~onBox.

% Grasping the bananas causes the monkey to have the bananas.
graspBananas causes hasBananas.

% Grasping the bananas is not permissible if the monkey already has the bananas.
nonexecutable graspBananas if hasBananas.

% Grasping the bananas is not permissible if the monkey is not on the box.
nonexecutable graspBananas if ~onBox.

% Grasping the bananas is not permissible if the location of the monkey is not the same as the location of the bananas.
nonexecutable graspBananas if loc(monkey)\=loc(bananas).

:- query
	0: loc(monkey)=l1 & loc(box) = l2 & loc(bananas) = l3 & ~hasBananas & ~onBox;
	maxstep: hasBananas.

[EXAMPLE 3]

Problem description:
A fleet of vehicles which have some capacity can drive passengers to from locations to other locations. 

There are three main types of things: vehicle, location, and integer.

bus1 and bus2 are vehicles.
stop1, stop2, and stop3 are locations.
0..20 are integers.

Actions
Driving the vehicile is an action.

Query (in natural language):
Initially, 10 passengers are at stop1, 10 passengers are at stop2, and 0 passengers are at stop3. bus1 has capacity 3 and bus2 has capacity 4. Find a plan so that all 20 passengers are at stop3.

BC+ program:
:- sorts
    vehicle;
    location;
    integer.

:- variables
    V, V1, V2, V3, V4 :: vehicle;
    Loc, Loc1, Loc2, Loc3, Loc4 :: location;
    N, N1, N2, N3, N4 :: integer.

:- objects
    bus1, bus2 :: vehicle;
    stop1, stop2, stop3 :: location;
    0..20 :: integer.

:- constants
    loc(vehicle) :: inertialFluent(location);
    capacity(vehicle) :: inertialFluent(integer);
    drive(vehicle) :: exogenousAction;
    going(vehicle) :: attribute(location) of drive(vehicle);
    amount(vehicle) :: attribute(integer) of drive(vehicle);
    numAt(location) :: additiveFluent(integer);
    departing(location) :: additiveAction(integer).

% Driving a vehicle causes the location of the vehicle to change. ("causes" rule)
drive(V) causes loc(V)=Loc if going(V)=Loc.

% Driving a vehicle causes the number of passengers at the original location to decrease. ("decrement" rule. Since we use the drive action, we also use its attribute amount')
drive(V) decrements numAt(Loc1) by N if amount(V)=N & loc(V)=Loc1.

% Driving a vehicle causes the number of passengers at the destination location to increase. ("increment" rule. Since we use the drive action, we also use its attribute amount')
drive(V) increments numAt(Loc2) by N if amount(V)=N & going(V)=Loc2.

% Driving a vehicle is not executable if the number of passengers on the vehicle is greater than the capacity of the vehicle. (Use drive(vehicle). Since it is an action, we use nonexecutable.)
nonexecutable drive(V) if amount(V) > capacity(V).

% Driving a vehicle is not permissible if the amount of passengers on the vehicle is zero. (Use drive(vehicle). Since it is an action, we use nonexecutable.)
nonexecutable drive(V) if amount(V)=0.

% Driving increases the amount that are departing by the amount of passengers on board. ("increment" rule. Since we use the drive action, we also use its attribute amount')
drive(V) increments departing(Loc) by N if loc(V)=Loc & amount(V)=N.

% The amount of passengers departing must not be greater than the number of passengers at the location departing from. ("always" rule.)
always departing(Loc) <= numAt(Loc).

% The capacity of bus1 and bus2 have capacity 3 and 4.
capacity(bus1) = 3.
capacity(bus2) = 4.

:- query
	0: numAt(stop1) = 10 & numAt(stop2) = 10 & numAt(stop3) = 0;
	maxstep: numAt(stop3) = 20.


[INSTRUCTIONS]

Based on the problem description, previously generated BC+ signature and natural language rules/constraints to represent in BC+, generate the rules/constraints in BC+ along with the query.

[PROBLEM]

Description:
<PROBLEM DESCRIPTION>

Hint:
<HINT>

BC+ description:
<ACTIONS AND CONSTANTS>

<DOMAIN>

Rules/constraints to represent in BC+:
<CONSTRAINTS>

Query (in natural language):
<QUERY>

Do not alter or change the BC+ signature in any way, only present the constraints/rules (numbered), and query together in the following format, encapsulated in three backticks:

```
% constraints/rules
% 1. <comment for rule 1>
<BC+ rule 1>

% 2. <comment for rule 2>
<BC+ rule 1>
...

% query
< BC+ query>

```'''





sign_gen= f'''{bc_description}

[INSTRUCTIONS]
Given a hint, problem description, and knowledge about a domain, produce the relevant fluent and action constants and the BC+ signature. Do not use the same names for constants, even if they are of a different type or have different arguments. For example, on(block) and on(block,table) cannot both be declared.

[EXAMPLE 1]
Problem description:
A monkey wants to get a bunch of bananas hanging from the ceiling. He can reach the bananas by first pushing a box to the empty place under the bananas and then climbing on top of the box.

There are two main types of objects: thing and location.

monkey, bananas, and box are objects.
l1, l2, and l3 are locations.

Actions description:
Walking to a location
Pushing the box to a location
Climbing on the box
Climbing off the box
Grabbing the bananas

Things we need to represent:
Walking should change the location of the monkey, but it cannot walk if it is on the box.
Pushing the box should change the location of the box and the monkey.
Climbing on/off the box causes he monkey to be on/off of it.
Grabbing the bananas means that the monkey will have the bananas.

Syntax analysis:
Apart from the actions, to describe this problem, we need to represent the location of the monkey, bananas, and box (things). Since locations of objects stay the same unless changed, they will be inertial fluents. If the monkey climbs onto the box, we should have a way to represent this as well. The monkey remains on the box unless something changes that, so it is inertial as well. Finally, whether the monkey has the bananas needs to be represented, which is also an inertial fluent.

Actions:
walk(location) - The monkey can walk to a location.
pushBox(Loc) - The monkey can push the box to a location.
climbOn - The monkey can climb onto the box.
climbOff - The monkey can climb off of the box.
graspBananas - The monkey can grasp the bananas.

Constants:
loc(thing) - The location of something, which stays the same unless explicitly changed, so it is an inertial fluent.
hasBananas - The monkey having the bananas, which stays the same unless explicitly changed, so it is an inertial fluent.
onBox - The monkey being on the box, which stays the same unless explicitly changed, so it is an inertial fluent.

BC+ Signature:

:- sorts
    thing;
    location.

:- objects
    monkey,bananas,box :: thing;
    l1,l2,l3 :: location.

:- variables
    T, T1, T2 :: thing;
    Loc, Loc1, Loc2 :: location;
    Bool, Bool1, Bool2 :: boolean.

:- constants
    walk(location) :: exogenousAction;
    pushBox(location) :: exogenousAction;
    climbOn :: exogenousAction;
    climbOff :: exogenousAction;
    graspBananas :: exogenousAction;
    loc(thing) :: inertialFluent(location);
    hasBananas :: inertialFluent(boolean);
    onBox :: inertialFluent(boolean).

[Example 2]

Problem description:
Blocks can be stacked on each other or directly on a table. The task is to stack blocks on each other in a specified order.

There are two main types of objects: "block" and "loc".
loc includes block.
 
b1, b2, b3, and b4 are blocks.
table is a loc.

Actions description:
Moving a block to a location

Parts of the problem we need to represent:
Blocks have a location (which can be another block). 
Moving a block causes it's location to change.

Syntax analysis:
Apart from the actions, to describe this problem, we need to represent the location of blocks, which remain the same over time unless explicitly changed, so it is inertial.

Actions:
move(block,location) - Move a block to a location.

Constants:
loc(block) - The location of a block, which remains the same unless explicitly changed, so it is an inertial fluent.

BC+ Signature:

:- sorts
    loc >> block.
:- objects
    b1, b2, b3, b4 :: block;
    table :: loc.
:- constants
    loc(block) :: inertialFluent(loc);
    move(block, loc) :: exogenousAction.
:- variables
    B, B1, B2, B3, B4       :: block;
    L, L1, L2, L3, L4           :: loc;
    Bool, Bool1, Bool2, Bool3, Bool4 :: boolean.

[Example 3]

Problem description:
There are vehicles which can take passengers to different stops. Each bus has a capacity of passengers. A certain number of passengers will need to be transported to a certain location.

There are three main types of objects: locations, vehicles, and integer.

stop1, stop2, and stop3 are locations.
bus1 and bus2 are vehicles.
0..20 are integers.

Actions description:
Driving a vehicle.

Parts of the problem we need to represent:
The vehicle capacity.
The vehicle location.
A vehicle can drive from one location to another.
The number of passengers should change based on how many are in a vehicle.
The total number of passengers departing at once since there are multiple vehicles.

Syntax analysis:
Apart from the actions, to describe this problem, we need to represent the capacity of each vehicle, which remains the same unless explicitly changed, so it is an inertial fluent. We also need to represent the location of a vehicle, which also remains the same unless changed, so it is inertial. Where the vehicle is driving to is about the action of driving, so it is an attribute of it. Each vehicle will be carrying some number of passengers, which is tied to a specific action, so it is an attribute of it. The number of passengers at a location is about state information and can increase/decrease, so it is an additive fluent. The total number of passengers departing is at the action level, but can be affected by multiple actions, so it is an additive action.

Actions:
drive(vehicle) - Drive a vehicle.

Constants:
loc(vehicle)- The location of a vehicle stays the same unless explicitly changed, so it is an inertialFluent(location).
capacity(vehicle) - The capacity of a vehicle stays the same unless explicitly changed, so it is an inertialFluent(integer).
drivingTo(vehicle) - Where a vehicle is going is related to the driving action, so it is an attribute of it.
amount(vehicle) - How many passengers in a vehicle is related to the drive action action, so it is an attribute of it.
numAt(location) - The number of passengers at a location can be affected by multipe actions, and is about state information, so it is an additive fluent.
departing(location) - The number of passengers departing is about the driving action, and can be affected by multiple driving actions, so it is an additive action.

BC+ Signature:

:- sorts
    vehicle;
    location;
    integer.

:- variables
    V, V1, V2, V3, V4 :: vehicle;
    Loc, Loc1, Loc2, Loc3, Loc4 :: location;
    N, N1, N2, N3, N4 :: integer.

:- objects
    bus1, bus2 :: vehicle;
    stop1, stop2, stop3 :: location;
    0..20 :: integer.

:- constants
    loc(vehicle) :: inertialFluent(location);
    capacity(vehicle) :: inertialFluent(integer);
    drive(vehicle) :: exogenousAction;
    drivingTo(vehicle) :: attribute(location) of drive(vehicle);
    amount(vehicle) :: attribute(integer) of drive(vehicle);
    numAt(location) :: additiveFluent(integer);
    departing(location) :: additiveAction(integer).

[Problem]
<DOMAIN>

<HINT>

As shown in the examples, write the actions, constants, and BC+ signature. Make sure to include enough variables for each sort, which will be needed later to write rules (5 variables each should be enough, for example, N, N1, N2, N3, N4 for integer, etc.).
Encapsulate your answer in 3 backticks like the following:

```
Actions:
<actions>

Constants:
<constants with their reading>

BC+ Signature:
<signature>
```
'''



knowledge_gen = '''Given a description of a problem, write knowledge about the domain that we would expect to represent in an action language BC+ program. These should represent logical constraints and cause and effect in the problem.

For example, a task about moving objects would involve some knowledge about what is required to move, what the effect of moving an object does, such as the location of the object changing or its previous location now being empty. These restrictions and effects are dependent on the context of the problem. Here we list some example problems and extract knowledge.

[Example 1]
Description:
A monkey wants to get a bunch of bananas hanging from the ceiling. He can reach the bananas by first pushing a box to the empty place under the bananas and then climbing on top of the box. The task is to come up with a plan for retrieving the bananas.
Some things to consider are the monkey, the bananas, the box, the location of objects, and the monkey's ability to move and push the box. Provide the relevant knowledge. Only use the terminology in the description/hint to write the knowledge.

Hint:
There are two main types of things: "things" and "location".

monkey, bananas, and box are things.
l1, l2, and l3 are locations.

Actions:
walk to a location
push box to a location
climb on the box
climb off the box
grasp the bananas

Additional constants:
loc(thing) - The location of something should stay the same unless explicitly changed, it is inertial. The location of a thing should be a location, therefore it will be declared as an inertialFluent(location).
hasBananas - The monkey having the bananas should stay the same unless explicitly changed, it is inertial. Since whether the monkey has bananas or not is either true or false, it will be declared as inertialFluent(boolean).
onBox - The monkey being on the box should stay the same unless explicitly changed, it is inertial. Since whether the monkey is on the box or not either true or false, it will be declared as inertialFluent(boolean).

BC+ signature:
:- sorts
    thing;
    location.

:- objects
    monkey,bananas,box :: thing;
    l1,l2,l3 :: location.

:- variables
    T, T1, T2 :: thing;
    Loc, Loc1, Loc2 :: location;
    Bool, Bool1, Bool2 :: boolean.

:- constants
    loc(thing) :: inertialFluent(location);
    hasBananas,onBox :: inertialFluent(boolean);
    walk(location) :: exogenousAction;
    pushBox(location) :: exogenousAction;
    climbOn :: exogenousAction;
    climbOff :: exogenousAction;
    graspBananas :: exogenousAction.

Generated knowledge:
% The location of the bananas is where the monkey is if the monkey has bananas.
% The location of the monkey is where the box is if the monkey is on the box.
% Walking to a location causes the monkey's location to change.
% Walking is not executable to a location if the monkey is already in that location.
% Walking is not executable if the monkey is on the box.
% Pushing the box to a location causes the location of the box to move.
% Pushing the box to a location causes the location f the monkey to move.
% Pushing the box is not executable to a location if the monkey is at that location
% Pushing the box is not executable if the monkey is on the box.
% Pushing the box is not executable if the location of the monkey is not the same as the location of the box.
% Climbing on the box causes the monkey to be on the box.
% Climbing on the box is not executable if the monkey is already on the box.
% Climbing on the box is not executable if the location of the monkey is not the same as the box.
% Climbing off of the box causes the monkey to not be on the box.
% Climbing off of the box is not executable if the monkey is not on the box.
% Grasping the bananas causes the monkey to have the bananas.
% Grasping the bananas is not executable if the monkey already has the bananas.
% Grasping the bananas is not executable if the monkey is not on the box.
% Grasping the bananas is not executable if the location of the monkey is not the same as the location of the bananas.
% It is not executable to both walk to a location and push the box to a location.
% It is not executable to both walk to a location and climb on the box.
% It is not executable to both push the box to a location and climb on the box.
% It is not executable to both climb off of the box and grasp the bananas.

[Example 2]
Description:
Blocks can be stacked on each other or directly on a table. The task is to stack blocks on each other in a specified order. Provide the relevant knowledge. Only use the terminology in the description/hint to write the knowledge.

Hint:
There are two main types of things: "block" and "loc".
"loc" includes "block".

b1, b2, b3, and b4 are blocks.
table is a loc.

Actions:
Moving a block to a location

Additional constants:
loc(block) - The location of a block remains the same unless explicitly changed, so it is inertial. The value of the location of a block is a location, so loc(block) is declared as inertialFluent(loc).

BC+ signature:
:- sorts
    loc >> block.
:- objects
    b1, b2, b3, b4 :: block;
    table :: loc.
:- constants
    loc(block) :: inertialFluent(loc);
    move(block, loc) :: exogenousAction.
:- variables
    B, B1, B2, B3, B4       :: block;
    L, L1, L2, L3, L4           :: loc;
    Bool, Bool1, Bool2, Bool3, Bool4 :: boolean.

Generated knowledge:
% It is impossible for two blocks to be at the same location.
% Moving a block causes it's location to be at that location.
% The move action is not executable if something is on the location to be moved to.
% The move action is not executable if something is on top of the block which is being moved.

[Problem]
Description:
<PROBLEM DESCRIPTION> Provide the relevant knowledge. Only use the terminology in the hint/description to write the knowledge.

Hint:
<HINT>

BC+ description
<ACTIONS AND CONSTANTS>

<DOMAIN>

Generate the the knowledge relevant to this problem, ONLY using natural langauge. Do not mention any of the program within this knowledge, though the signature should be considered when writing the knowledge. Encapsulate it in three backticks like so:

```
% generated knowledge
% <knowledge #1>
% <knowledge #2>
...
```'''


sq = f'''{bc_description}

QUERIES:
Queries have three components: an optional label, an optional maximum step which list formulas which should be true in the last step of the plan, and a set of constraint formulas to apply, each parametrized with the step at which they should be applied.
For example the following query represents an initial state and an action at step 0, and a set of constraints which should be met at the end of the plan.

:- query
	label :: test_query;
	0: loc(b1)=b2 & loc(b2)=b3 & loc(b3)=a & loc(b4)=b & loc(b5)=c;
	0: move(b1, b5);
	maxstep: loc(b5,c) & loc(b4,b5) & loc(b3,b4) & loc(b2,b3) & loc(b1,b2).

[INSTRUCTIONS]

Based on the problem description, and generated BC+ program. Generate some simple queries which can be used to make sure the program is working properly. For example, consider the following example.

[EXAMPLE 1]

Problem description:
Blocks can be stacked on top of each other or on a table. Blocks stacked on the table are in a tower.

There are two main types of things: loc and block.
loc includes block.

b1, b2, b3, and b4 are blocks.
table is a loc.

Actions
Moving a block to a location.

Initially, block b1 is on b2, b2 is on the table, b3 is on the table, and b4 is on b3. Find a plan so that block b1 is on b4, b2 is on b3, b3 is on b1, and b4 is on the table.

BC+ Program:
:- sorts
    loc >> block.
:- objects
    b1, b2, b3, b4 :: block;
    table :: loc.
:- constants
    loc(block) :: inertialFluent(loc);
    in_tower(block) :: inertialFluent(boolean);
    move(block, loc) :: exogenousAction.
:- variables
    B, B1, B2, B4 :: block;
    L, L1, L2, L3 :: loc.

% Two blocks cannot be at the same location. (Use loc(block). Since it is a fluent, we use impossible. Since we use impossible, we only use "&". "if" is not allowed). Use "\=" to differentiate B1 and B2.
impossible loc(B1) = B & loc(B2) = B & B1\=B2. 

% A block is in a tower if it's location is on the table. ("Static law")
in_tower(B) if loc(B) = table.

% A block is in a tower if it's location is on something that is in a tower. ("Static law")
in_tower(B) if loc(B) = B1 & in_tower(B1).

% Blocks don't float in the air. (Use in_tower(block). Since it is a fluent, we use impossible. Since we use impossible, we only use "&". "if" is not allowed)
impossible ~in_tower(B).

% Moving a block causes it's location to move to loc. ("causes" rule)
move(B,L) causes loc(B)=L.

% The move action is not permissible if something is on the location to be moved to. (Use move(block, loc). Since it is an action, we use nonexecutable.)
nonexecutable move(B,L) if loc(B1) = B.

% A block is in tower after it is in tower and it is on a block.
in_tower(B) after in_tower(B) and loc(B)=B1.

% By default, all blocks are in a tower.
default ~in_tower(B).

:- query
	0: loc(b1) = b2 & loc(b2) = table & loc(b3) = table & loc(b4)=b3);
	maxstep: loc(b1) = b4 & loc(b2) = b3 & loc(b3)=b1 & loc(b4) = table. 

Sample queries:

% Query 1: Move a single block which should be able to be moved. Block b4 should be able to be moved to the table. (satisfiable)
:- query
	0: loc(b1) = b2 & loc(b2) = table & loc(b3) = table & loc(b4)=b3);
    0: move(b4, table).

% Query 2: Move a single block which should NOT be able to be moved. Block b2 should not be able to be moved on top of block b3, since b1 is on top of b2. (unsatisfiable)
:- query
	0: loc(b1) = b2 & loc(b2) = table & loc(b3) = table & loc(b4)=b3);
    0: move(b2, b3).

% Query 3: End up in a state where two blocks are on the same block, which should NOT be allowed. Block b2 is on b1, let's try to move block b3 onto b1. (unsatisfiable)
:- query
	0: loc(b1) = b2 & loc(b2) = table & loc(b3) = table & loc(b4)=b3);
    0: move(b3, b1).

[PROBLEM]

Description:
<PROBLEM DESCRIPTION>

BC+ description:
<ACTIONS AND CONSTANTS>

<DOMAIN>

Rules/constraints to represent in BC+:
<CONSTRAINTS>

Main Query:
<QUERY>
<BC QUERY>

Based on the problem description, and generated BC+ program. Generate some simple queries which can be used to make sure the program is working properly. Only generate a few, no more than 5. Append either (satisfiable) or (unsatisfiable) to the end of the query in natural language, depending on whether the query should work or not. Keep in mind, the starting states of the sample queries should be allowable based on the already written constraints in the program (e.g., if a query comes back unsatisfiable, it shouldn't be because the start state was unsatisfiable). Do so in the following format, encapsulated in 3 backticks:
```
% Query 1: <natural language query> (satisfiable/unsatisfiable)
<BC+ Query>

% Query 2: <natural language query> (satisfiable/unsatisfiable)
<BC+ Query>
...

```'''

sq_feedback = '''<BC+ DESCRIPTION>

QUERIES:
Queries have three components: an optional label, an optional maximum step which list formulas which should be true in the last step of the plan, and a set of constraint formulas to apply, each parametrized with the step at which they should be applied.
For example the following query represents an initial state and an action at step 0, and a set of constraints which should be met at the end of the plan.

:- query
	label :: test_query;
	0: loc(b1)=b2 & loc(b2)=b3 & loc(b3)=a & loc(b4)=b & loc(b5)=c;
	0: move(b1, b5);
	maxstep: loc(b5,c) & loc(b4,b5) & loc(b3,b4) & loc(b2,b3) & loc(b1,b2).

[EXAMPLE 1]

Problem description:
Blocks can be stacked on top of each other or on a table. Blocks stacked on the table are in a tower.

There are two main types of things: loc and block.
loc includes block.

b1, b2, b3, and b4 are blocks.
table is a loc.

Actions
Moving a block to a location.

Query
Initially, block b1 is on b2, b2 is on the table, b3 is on the table, and b4 is on b3. Find a plan so that block b1 is on b4, b2 is on b3, b3 is on b1, and b4 is on the table.

BC+ Program:
:- sorts
    loc >> block.
:- objects
    b1, b2, b3, b4 :: block;
    table :: loc.
:- constants
    loc(block) :: inertialFluent(loc);
    in_tower(block) :: inertialFluent(boolean);
    move(block, loc) :: exogenousAction.
:- variables
    B, B1, B2, B4 :: block;
    L, L1, L2, L3 :: loc.

% Two blocks cannot be at the same location. (Use loc(block). Since it is a fluent, we use impossible. Since we use impossible, we only use "&". "if" is not allowed). Use "\=" to differentiate B1 and B2.
impossible loc(B1) = B & loc(B2) = B & B1\=B2. 

% A block is in a tower if it's location is on the table. ("Static law")
in_tower(B) if loc(B) = table.

% A block is in a tower if it's location is on something that is in a tower. ("Static law")
in_tower(B) if loc(B) = B1 & in_tower(B1).

% Blocks don't float in the air. (Use in_tower(block). Since it is a fluent, we use impossible. Since we use impossible, we only use "&". "if" is not allowed)
impossible ~in_tower(B).

% Moving a block causes it's location to move to loc. ("causes" rule)
move(B,L) causes loc(B)=L.

% The move action is not permissible if something is on the location to be moved to. (Use move(block, loc). Since it is an action, we use nonexecutable.)
nonexecutable move(B,L) if loc(B1) = B.

% A block is in tower after it is in tower and it is on a block.
in_tower(B) after in_tower(B) and loc(B)=B1.

% By default, all blocks are in a tower.
default ~in_tower(B).

:- query
	0: loc(b1) = b2 & loc(b2) = table & loc(b3) = table & loc(b4)=b3);
	maxstep: loc(b1) = b4 & loc(b2) = b3 & loc(b3)=b1 & loc(b4) = table. 

[EXAMPLE 2]

Problem description:
A monkey wants to get a bunch of bananas hanging from the ceiling. He can reach the bananas by first pushing a box to the empty place under the bananas and then climbing on top of the box.

There are three main types of things: "monkey", "thing" and "location".
"thing" includes "monkey".

monkey, bananas, and box are things.
l1, l2, and l3 are locations.

Actions
walk to a location
push box to a location
climb on
climb off
grasp bananas

Query
Initially, the monkey is at location l1, the box is at l2, and the bananas are at location l3. Generate a plan so that the monkey has the bananas.

BC+ program:
:- sorts
    thing;
    location.

:- objects
    monkey,bananas,box :: thing;
    l1,l2,l3 :: location.

:- variables
    Loc, Loc1, Loc2 :: location;
    Bool, Bool1, Bool2 :: boolean.

:- constants
    loc(thing) :: inertialFluent(location);
    hasBananas,onBox :: inertialFluent;
    walk(location) :: exogenousAction;
    pushBox(location) :: exogenousAction;
    climbOn :: exogenousAction;
    climbOff :: exogenousAction;
    graspBananas :: exogenousAction.

% The location of the bananas is where the monkey is if the monkey has bananas.
loc(bananas)=Loc if hasBananas & loc(monkey)=Loc.

% The location of the monkey is where the box is if the monkey is on the box. 
loc(monkey)=Loc if onBox & loc(box)=Loc.

% The monkey cannot be in two places at once.
impossible loc(monkey) = Loc1 & loc(monkey)=Loc2 & Loc1\=Loc2.

% Walking to a location causes the monkey's location to change.
walk(Loc) causes loc(monkey)=Loc.

% Walking is not permissible to a location if the monkey is already in that location.
nonexecutable walk(Loc) if loc(monkey)=Loc.

% Walking is not permissible if the monkey is on the box.
nonexecutable walk(Loc) if onBox.

% Pushing the box to a location causes the location of the box to move.
pushBox(Loc) causes loc(box)=Loc.

% Pushing the box to a location causes the location of the monkey to move.
pushBox(Loc) causes loc(monkey)=Loc.

% Pushing the box is not permissible to a location if the monkey is at that location.
nonexecutable pushBox(Loc) if loc(monkey)=Loc.

% Pushing the box is not permissible if the monkey is on the box.
nonexecutable pushBox(Loc) if onBox.

% Pushing the box is not permissible if the location of the monkey is not the same as the location of the box.
nonexecutable pushBox(Loc) if loc(monkey)\=loc(box).

% Climbing on the box causes the monkey to be on the box.
climbOn causes onBox.

% Climbing on the box is not permissible if the monkey is already on the box.
nonexecutable climbOn if onBox.

% Climbing on the box is not permissible if the location of the monkey is not the same as the box.
nonexecutable climbOn if loc(monkey)\=loc(box).

% Climbing off of the box causes the monkey to not be on the box.
climbOff causes ~onBox.

% Climbing off of the box is not permissible if the monkey is not on the box.
nonexecutable climbOff if ~onBox.

% Grasping the bananas causes the monkey to have the bananas.
graspBananas causes hasBananas.

% Grasping the bananas is not permissible if the monkey already has the bananas.
nonexecutable graspBananas if hasBananas.

% Grasping the bananas is not permissible if the monkey is not on the box.
nonexecutable graspBananas if ~onBox.

% Grasping the bananas is not permissible if the location of the monkey is not the same as the location of the bananas.
nonexecutable graspBananas if loc(monkey)\=loc(bananas).

:- query
	0: loc(monkey)=l1 & loc(box) = l2 & loc(bananas) = l3 & ~hasBananas & ~onBox;
	maxstep: hasBananas.

[EXAMPLE 3]

Problem description:
A fleet of vehicles which have some capacity can drive passengers to from locations to other locations. 

There are three main types of things: vehicle, location, and integer.

bus1 and bus2 are vehicles.
stop1, stop2, and stop3 are locations.
0..20 are integers.

Actions
Driving the vehicile is an action.

Query
Initially, 10 passengers are at stop1, 10 passengers are at stop2, and 0 passengers are at stop3. bus1 has capacity 3 and bus2 has capacity 4. Find a plan so that all 20 passengers are at stop3.

BC+ program:
:- sorts
    vehicle;
    location;
    integer.

:- variables
    V, V1, V2, V3, V4 :: vehicle;
    Loc, Loc1, Loc2, Loc3, Loc4 :: location;
    N, N1, N2, N3, N4 :: integer.

:- objects
    bus1, bus2 :: vehicle;
    stop1, stop2, stop3 :: location;
    0..20 :: integer.

:- constants
    loc(vehicle) :: inertialFluent(location);
    capacity(vehicle) :: inertialFluent(integer);
    drive(vehicle) :: exogenousAction;
    going(vehicle) :: attribute(location) of drive(vehicle);
    amount(vehicle) :: attribute(integer) of drive(vehicle);
    numAt(location) :: additiveFluent(integer);
    departing(location) :: additiveAction(integer).

% Driving a vehicle causes the location of the vehicle to change. ("causes" rule)
drive(V) causes loc(V)=Loc if going(V)=Loc.

% Driving a vehicle causes the number of passengers at the original location to decrease. ("decrement" rule. Since we use the drive action, we also use its attribute amount')
drive(V) decrements numAt(Loc1) by N if amount(V)=N & loc(V)=Loc1.

% Driving a vehicle causes the number of passengers at the destination location to increase. ("increment" rule. Since we use the drive action, we also use its attribute amount')
drive(V) increments numAt(Loc2) by N if amount(V)=N & going(V)=Loc2.

% Driving a vehicle is not executable if the number of passengers on the vehicle is greater than the capacity of the vehicle. (Use drive(vehicle). Since it is an action, we use nonexecutable.)
nonexecutable drive(V) if amount(V) > capacity(V).

% Driving a vehicle is not permissible if the amount of passengers on the vehicle is zero. (Use drive(vehicle). Since it is an action, we use nonexecutable.)
nonexecutable drive(V) if amount(V)=0.

% Driving increases the amount that are departing by the amount of passengers on board. ("increment" rule. Since we use the drive action, we also use its attribute amount')
drive(V) increments departing(Loc) by N if loc(V)=Loc & amount(V)=N.

% The amount of passengers departing must not be greater than the number of passengers at the location departing from. ("always" rule.)
always departing(Loc) <= numAt(Loc).

% The capacity of bus1 and bus2 have capacity 3 and 4.
capacity(bus1) = 3.
capacity(bus2) = 4.

:- query
	0: numAt(stop1) = 10 & numAt(stop2) = 10 & numAt(stop3) = 0;
	maxstep: numAt(stop3) = 20.

<CHECKLIST>

[INSTRUCTIONS]
Consider the problem and BC+ program, and simple sample queries which were ran to check the basic functionality of the program. The output of each sample query and the main query is presented. Check that the Cplus2ASP output makes sense.

[Problem]
<PROBLEM DESCRIPTION>

BC+ Program:
<BC+ PROGRAM>

Sample queries and outputs:
<FEEDBACK>

Main query and output:
% Original natural language query: <QUERY>
<FEEDBACK MAIN QUERY>

[INSTRUCTIONS (continued)]
1) [FEEDBACK OUTLINE]
Based on the feedback, if any of the following segments are incorrect, then mark them with "[CHANGED]", and revise them:
- PROGRAM
- MAIN QUERY
- SAMPLE QUERIES

Otherwise, if a segment is correct, mark it with "[UNCHANGED]", and simply copy their contents. 

2) [SAMPLE QUERY GUIDANCE]
Keep in mind, the outputs from running the sample queries is to help check that the program is working properly. In some cases, the sample queries themselves may be wrong (e.g., a syntax error), and can be re-written. The sample queries marked (satisfiable) should be correctly be satisfiable and the queries marked (unsatisfiable) should be unsatisfiable. There should not be apparent violations in the constraints, and the action preconditions/effects should enforced properly. If there are, then revise the main program. Overall, changes should be succint, e.g., only change relevant parts while leaving the remainder alone.

3) [MAIN QUERY OUTPUT]
IMPORTANT: Check that each action in the final plan of the main query makes sense given the state before it, and that the resulting state correctly follows.
If something doesn't align with the common sense relative to the problem description, then update the program. Though less likely, if you suspect there is an issue with the main BC+ query, it may be changed, but it should have the original meaning of the main query as shown under "Main query and output", after "Original natural language query: ". The query itself should not contain actions, but have only the initial state and the final state (indicated with "maxstep").

4) [FORMAT]
The format should be like the following, encapsulated in 3 backticks:

```% PROGRAM CHANGED? [CHANGED/UNCHANGED]
% BC+ signature
<Enter BC+ signature>

% Generated constraints
<Enter BC+ rules/constraints>

% MAIN QUERY CHANGED? [CHANGED/UNCHANGED]
<Enter the main query>

% SAMPLE QUERIES CHANGED? [CHANGED/UNCHANGED]
<Enter the sample queries (do NOT include the Cplus2ASP outputs)>
```'''.replace('<BC+ DESCRIPTION>',bc_description).replace('<CHECKLIST>', checklist)










feedback_qsat = '''<BC+ DESCRIPTION>
Example Programs:

[EXAMPLE 1]

Problem description:
Blocks can be stacked on top of each other or on a table. Blocks stacked on the table are in a tower.

There are two main types of things: loc and block.
loc includes block.

b1, b2, b3, and b4 are blocks.
table is a loc.

Actions
Moving a block to a location.

Query
Initially, block b1 is on b2, b2 is on the table, b3 is on the table, and b4 is on b3. Find a plan so that block b1 is on b4, b2 is on b3, b3 is on b1, and b4 is on the table.

BC+ Program:
:- sorts
    loc >> block.
:- objects
    b1, b2, b3, b4 :: block;
    table :: loc.
:- constants
    loc(block) :: inertialFluent(loc);
    in_tower(block) :: inertialFluent(boolean);
    move(block, loc) :: exogenousAction.
:- variables
    B, B1, B2, B4 :: block;
    L, L1, L2, L3 :: loc.

% Two blocks cannot be at the same location. (Use loc(block). Since it is a fluent, we use impossible. Since we use impossible, we only use "&". "if" is not allowed). Use "\=" to differentiate B1 and B2.
impossible loc(B1) = B & loc(B2) = B & B1\=B2. 

% A block is in a tower if it's location is on the table. ("Static law")
in_tower(B) if loc(B) = table.

% A block is in a tower if it's location is on something that is in a tower. ("Static law")
in_tower(B) if loc(B) = B1 & in_tower(B1).

% Blocks don't float in the air. (Use in_tower(block). Since it is a fluent, we use impossible. Since we use impossible, we only use "&". "if" is not allowed)
impossible ~in_tower(B).

% Moving a block causes it's location to move to loc. ("causes" rule)
move(B,L) causes loc(B)=L.

% The move action is not permissible if something is on the location to be moved to. (Use move(block, loc). Since it is an action, we use nonexecutable.)
nonexecutable move(B,L) if loc(B1) = B.

% A block is in tower after it is in tower and it is on a block.
in_tower(B) after in_tower(B) and loc(B)=B1.

% By default, all blocks are in a tower.
default ~in_tower(B).

:- query
	0: loc(b1) = b2 & loc(b2) = table & loc(b3) = table & loc(b4)=b3);
	maxstep: loc(b1) = b4 & loc(b2) = b3 & loc(b3)=b1 & loc(b4) = table. 

[EXAMPLE 2]

Problem description:
A monkey wants to get a bunch of bananas hanging from the ceiling. He can reach the bananas by first pushing a box to the empty place under the bananas and then climbing on top of the box.

There are three main types of things: "monkey", "thing" and "location".
"thing" includes "monkey".

monkey, bananas, and box are things.
l1, l2, and l3 are locations.

Actions
walk to a location
push box to a location
climb on
climb off
grasp bananas

Query
Initially, the monkey is at location l1, the box is at l2, and the bananas are at location l3. Generate a plan so that the monkey has the bananas.

BC+ program:
:- sorts
    thing;
    location.

:- objects
    monkey,bananas,box :: thing;
    l1,l2,l3 :: location.

:- variables
    Loc, Loc1, Loc2 :: location;
    Bool, Bool1, Bool2 :: boolean.

:- constants
    loc(thing) :: inertialFluent(location);
    hasBananas,onBox :: inertialFluent;
    walk(location) :: exogenousAction;
    pushBox(location) :: exogenousAction;
    climbOn :: exogenousAction;
    climbOff :: exogenousAction;
    graspBananas :: exogenousAction.

% The location of the bananas is where the monkey is if the monkey has bananas.
loc(bananas)=Loc if hasBananas & loc(monkey)=Loc.

% The location of the monkey is where the box is if the monkey is on the box. 
loc(monkey)=Loc if onBox & loc(box)=Loc.

% The monkey cannot be in two places at once.
impossible loc(monkey) = Loc1 & loc(monkey)=Loc2 & Loc1\=Loc2.

% Walking to a location causes the monkey's location to change.
walk(Loc) causes loc(monkey)=Loc.

% Walking is not permissible to a location if the monkey is already in that location.
nonexecutable walk(Loc) if loc(monkey)=Loc.

% Walking is not permissible if the monkey is on the box.
nonexecutable walk(Loc) if onBox.

% Pushing the box to a location causes the location of the box to move.
pushBox(Loc) causes loc(box)=Loc.

% Pushing the box to a location causes the location of the monkey to move.
pushBox(Loc) causes loc(monkey)=Loc.

% Pushing the box is not permissible to a location if the monkey is at that location.
nonexecutable pushBox(Loc) if loc(monkey)=Loc.

% Pushing the box is not permissible if the monkey is on the box.
nonexecutable pushBox(Loc) if onBox.

% Pushing the box is not permissible if the location of the monkey is not the same as the location of the box.
nonexecutable pushBox(Loc) if loc(monkey)\=loc(box).

% Climbing on the box causes the monkey to be on the box.
climbOn causes onBox.

% Climbing on the box is not permissible if the monkey is already on the box.
nonexecutable climbOn if onBox.

% Climbing on the box is not permissible if the location of the monkey is not the same as the box.
nonexecutable climbOn if loc(monkey)\=loc(box).

% Climbing off of the box causes the monkey to not be on the box.
climbOff causes ~onBox.

% Climbing off of the box is not permissible if the monkey is not on the box.
nonexecutable climbOff if ~onBox.

% Grasping the bananas causes the monkey to have the bananas.
graspBananas causes hasBananas.

% Grasping the bananas is not permissible if the monkey already has the bananas.
nonexecutable graspBananas if hasBananas.

% Grasping the bananas is not permissible if the monkey is not on the box.
nonexecutable graspBananas if ~onBox.

% Grasping the bananas is not permissible if the location of the monkey is not the same as the location of the bananas.
nonexecutable graspBananas if loc(monkey)\=loc(bananas).

:- query
	0: loc(monkey)=l1 & loc(box) = l2 & loc(bananas) = l3 & ~hasBananas & ~onBox;
	maxstep: hasBananas.

[EXAMPLE 3]

Problem description:
A fleet of vehicles which have some capacity can drive passengers to from locations to other locations. 

There are three main types of things: vehicle, location, and integer.

bus1 and bus2 are vehicles.
stop1, stop2, and stop3 are locations.
0..20 are integers.

Actions
Driving the vehicile is an action.

Query
Initially, 10 passengers are at stop1, 10 passengers are at stop2, and 0 passengers are at stop3. bus1 has capacity 3 and bus2 has capacity 4. Find a plan so that all 20 passengers are at stop3.

BC+ program:
:- sorts
    vehicle;
    location;
    integer.

:- variables
    V, V1, V2, V3, V4 :: vehicle;
    Loc, Loc1, Loc2, Loc3, Loc4 :: location;
    N, N1, N2, N3, N4 :: integer.

:- objects
    bus1, bus2 :: vehicle;
    stop1, stop2, stop3 :: location;
    0..20 :: integer.

:- constants
    loc(vehicle) :: inertialFluent(location);
    capacity(vehicle) :: inertialFluent(integer);
    drive(vehicle) :: exogenousAction;
    going(vehicle) :: attribute(location) of drive(vehicle);
    amount(vehicle) :: attribute(integer) of drive(vehicle);
    numAt(location) :: additiveFluent(integer);
    departing(location) :: additiveAction(integer).

% Driving a vehicle causes the location of the vehicle to change. ("causes" rule)
drive(V) causes loc(V)=Loc if going(V)=Loc.

% Driving a vehicle causes the number of passengers at the original location to decrease. ("decrement" rule. Since we use the drive action, we also use its attribute amount')
drive(V) decrements numAt(Loc1) by N if amount(V)=N & loc(V)=Loc1.

% Driving a vehicle causes the number of passengers at the destination location to increase. ("increment" rule. Since we use the drive action, we also use its attribute amount')
drive(V) increments numAt(Loc2) by N if amount(V)=N & going(V)=Loc2.

% Driving a vehicle is not executable if the number of passengers on the vehicle is greater than the capacity of the vehicle. (Use drive(vehicle). Since it is an action, we use nonexecutable.)
nonexecutable drive(V) if amount(V) > capacity(V).

% Driving a vehicle is not permissible if the amount of passengers on the vehicle is zero. (Use drive(vehicle). Since it is an action, we use nonexecutable.)
nonexecutable drive(V) if amount(V)=0.

% Driving increases the amount that are departing by the amount of passengers on board. ("increment" rule. Since we use the drive action, we also use its attribute amount')
drive(V) increments departing(Loc) by N if loc(V)=Loc & amount(V)=N.

% The amount of passengers departing must not be greater than the number of passengers at the location departing from. ("always" rule.)
always departing(Loc) <= numAt(Loc).

% The capacity of bus1 and bus2 have capacity 3 and 4.
capacity(bus1) = 3.
capacity(bus2) = 4.

:- query
	0: numAt(stop1) = 10 & numAt(stop2) = 10 & numAt(stop3) = 0;
	maxstep: numAt(stop3) = 20.

<CHECKLIST>

[INSTRUCTIONS]
Consider the problem and BC+ program, which when run with a basic query to check satisfiability (independent of the main query), fails.

[Problem]
<PROBLEM DESCRIPTION>

BC+ Program:
<BC+ PROGRAM>

Main query:
% Original natural language query: <QUERY>
<BC QUERY>

Feedback:
<FEEDBACK>

Based on the feedback, revise the program (signature and/or rules), and possibly the main query if needed to match a new signature, while retaining its original meaning under the main query (after "Original natural language query: "). The format should be like the following, with everything together, encapsulated in 3 backticks:

```% BC+ signature
<Enter BC+ signature>

% Generated constraints
<Enter BC+ rules/constraints>

% Main query
<Enter the main query>```'''.replace('<BC+ DESCRIPTION>',bc_description).replace('<CHECKLIST>',checklist)


files_list = [['bc+_description', bc_description],
              ['knowledge_generation', knowledge_gen],
              ['signature_generation', sign_gen],
              ['rule_query_generation', rule_gen],
              ['sample_queries_feedback', sq_feedback],
              ['query_sat_feedback',feedback_qsat],
              ['sample_query_generation', sq]]
import os
for (fname, text) in files_list:
    #print(fname)
    
    with open(os.path.join('prompts',fname+'.txt'), 'w') as f:
        f.write(text)



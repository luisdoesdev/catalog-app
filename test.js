var room = "ballroom";  // initate the variable room
var suspect = "Mr. Kalehoff";  // initiate the varibale supspect

var weapon = "";  // initiate the variable weapon
var solved = false;  // initiate the variable solve

if(room === "dining room" && suspect === "Mr. Parkes") {  /// if the variable room is equal to "dinning room" and the varibale suspect is "MR Parker"
// since the variable room is not a 'dinnng room' this is a false thus the varibale will not change
weapon = "knife";  /// set Weapon to 'Knife'
solved = 'true' ;     /// set solved to true

} else if(room === "gallery" && suspect === "Ms. Van Cleve") {  // else if the variable room is euqal to 'gallery' and the variable suspect is "Ms Van Cleve"
// since  the variable room is not 'gallery' this is a false thus the variable will not change
weapon = "trophy";
solved = "true";

} else if(room === "billiards room" && suspect === "Mrs. Sparr") { // else if the variable roomm is queal to 'billiards room' and the variable suspect is 'Mrs. Sparr'
// since the variable roomm is not equal to 'billiards room' this is false thus the variable will not change
weapon = "pool stick";
solved = "true";

} else if(room === "ballroom" && suspect === "Mr. Kalehoff"){  // else if the variable room is equal to 'ballroom ' and the variable suspect is 'Mr. Kalehoff'
// since the variable room is 'ballroom' this is true and the supect is 'Mr. Kalehoff' this is true
// lets change the variable 
weapon = "poison"; // variable weapon goes from '' to 'poison'

solved = "true"; // varible solve goes from false to true
}

if (solved) {  // if  the varibale solved is set to true
console.log(suspect + " did it in the " + room + " with the " + weapon+"!" + solved); // log the supect plus 'did it in the ' plus variable room plus 'with the ' plus weappon
}
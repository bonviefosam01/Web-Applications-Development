//import { all_words } from './wordish/all_words.js';
let row = 0
let targetWord = ""
let targetLock = "unlocked"

function checkInput(word){
    return (word.length == 5 && /^[a-zA-Z]+$/.test(word) )
}

function incrementRow(){
    return row += 1
}

function counter(s, c){
    let count = 0
    for (let i = 0; i < s.length; i++){
        if (s[i].toLowerCase() === c.toLowerCase()){
            count ++
        }
    }
    return count
}

function buildMap(map, letter){
        if(map.has(letter)) {
            map.set(letter, map.get(letter) + 1)
        } else {
            map.set(letter, 1)
        }
}

//end the game if row equals =6 or if target word equals guess word
function checkEndGame(g, t){
    if (g === t){
        return "win"
    } else if (row == 5){
        return "lose"
    } else {return}
}

function resetGame(){
    // I want to reset the cells
    row = 0
    for(let i=0; i < 5; i++){
        for (let j=0; j < 6; j++){
            let cell = document.getElementById(`cell_${j}_${i}`)
            cell.innerHTML = ""
            cell.style.backgroundColor = 'grey'
        }
        
    }
}

//Status bar functionality
function startGame() {
    let status = document.getElementById("status").innerHTML //remember cannot use value on a div element

    //need a check for if target word was already set
    if(targetWord != ""){
        document.getElementById("status").innerHTML = "WARNING: Finish game before setting target word again"
        document.getElementById("status").style.backgroundColor = '#F1E5AC'
        document.getElementById("status").style.padding = '30px'
        document.getElementById("target_text").value = ""
        return
    }

    resetGame()

    let target_word = document.getElementById("target_text").value
    document.getElementById("target_text").placeholder = "LOCKED"

    if(!checkInput(target_word)){
        document.getElementById("status").innerHTML = "Invalid Input: Must contain 5 letters"
        document.getElementById("status").style.backgroundColor = 'lightcoral'
        document.getElementById("target_text").placeholder = "TRY AGAIN"
        targetWord = ""
        document.getElementById("target_text").value = ""
        return
    }

    document.getElementById("status").innerHTML = "Start"
    targetWord = target_word
    document.getElementById("target_text").value = ""
    document.getElementById("status").style.backgroundColor = 'lightgreen'
    return
}    


function guessWord() {
    let guess = document.getElementById("guess_text").value

    // I don't want numbers, cannot be more or less than 5 letters
    if(!checkInput(guess)){
        document.getElementById("status").innerHTML = "Invalid Input: Must contain 5 letters"
        document.getElementById("status").style.backgroundColor = 'lightcoral'
        return
    }

    if(targetWord === ""){
        document.getElementById("status").innerHTML = "Invalid: Set target word before taking a guess."
        document.getElementById("status").style.backgroundColor = 'lightcoral'
        return
    }

    document.getElementById("status").innerHTML = "Successful Input! Guess Again."
    document.getElementById("status").style.backgroundColor = 'lightgreen'

    //count the number of each letter as it goes along via dict
    let guessMap = new Map()
    let used = [false, false, false, false, false]
    
    for(let i=0; i < 5; i++){
        let cell = document.getElementById(`cell_${row}_${i}`)
        cell.innerHTML = guess[i].toUpperCase() //need to put letters in right place in box and make upper case

        buildMap(guessMap, guess[i])
        //console.log(cell.innerHTML, targetWord[i].toUpperCase())

        if (cell.innerHTML === targetWord[i].toUpperCase()){
            used[i] = true
        } 
    } 
    console.log(guessMap)
    console.log(used)
    
    guessMap = new Map()
    for(let i=0; i < 5; i++){
        let cell = document.getElementById(`cell_${row}_${i}`)

        buildMap(guessMap, guess[i])
        console.log(targetWord, guess[i])
        console.log(targetWord.includes(guess[i]))
        console.log("used", !used[i])
        console.log("counts: ", guessMap.get(guess[i]), counter(targetWord,guess[i]))
        if (used[i]) {
            cell.style.backgroundColor = 'green'
        } 
        else if (targetWord.includes(guess[i]) && !used[i] && guessMap.get(guess[i]) <= counter(targetWord,guess[i])) {
            cell.style.backgroundColor = 'gold'
            for (let j = 0; j < 5; j++){
                if (!used[j] && targetWord[j] === guess[i]){
                    cell.style.backgroundColor = 'gold'
                    
                    break
                }
                else {cell.style.backgroundColor = 'red'}
            }
        }    
        else {cell.style.backgroundColor = 'red'}
    }
    

    //check for game ending conditions
    if(checkEndGame(guess, targetWord) === "win"){
        document.getElementById("guess_text").value = ""
        document.getElementById("target_text").placeholder = "PLAY AGAIN"
        document.getElementById("status").innerHTML = "GAME OVER: YOU WIN!"
        document.getElementById("status").style.backgroundColor = 'lightgreen'
        targetWord = ""
        return
    }
    if (checkEndGame(guess, targetWord) === "lose"){
        document.getElementById("guess_text").value = ""
        document.getElementById("target_text").placeholder = "TRY AGAIN"
        document.getElementById("status").innerHTML = "GAME OVER: YOU LOSE :("
        document.getElementById("status").style.backgroundColor = 'lightcoral'
        targetWord = ""
        return
    } 

    document.getElementById("guess_text").value = ""
    incrementRow()
    return
}
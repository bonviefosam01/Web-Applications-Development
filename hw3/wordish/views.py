from django.shortcuts import render

def process_word_parameter(request, target_text):
    entry = request.POST.get(target_text, "")
    if len(entry) != 5 or not entry.isalpha():
        raise Exception("Invalid Input: Must contain 5 letters")
    return entry

def process_old_guesses(request):
    old_guesses = request.POST.get("old_guesses")
    print(old_guesses)
    if old_guesses:
        guess_lst = old_guesses.split(",")
        for guess in guess_lst:
            if len(guess) != 5 or not guess.isalpha():
                raise Exception("Old guesses field is corrupted!")
        return guess_lst
    return []

def counter(s):
    count_dict = {}
    for char in s:
        if char in count_dict:
            count_dict[char] += 1
        else:
            count_dict[char] = 1
    return count_dict

def count(s, c):
    count = 0
    for i in range(len(s)):
        if (s[i].upper() == c.upper()):
            count += 1
    return count
    

def checkEndGame(g, t, lst):
    if (g == t):
        return "win"
    elif (len(lst) > 5):
        return "lose"
    else: return

def compute_game_context(target_text, guesses=[]):
    matrix = [["" for _ in range(5)] for _ in range(6)] 
    letter_cnt_t = counter(target_text.upper())
    status = "Welcome to Wordish! Start Now!"
    guess_button = ""
    #default matrix
    matrix = [[{"id": f"cell_{row}_{col}", "letter": "", "color": "grey"} for col in range(5)] for row in range(6)]

    if guesses: #!= None or len(guesses) > 0:
        for row in range(len(guesses)):
            guess = guesses[row].upper()
            target = list(target_text.upper())
            colors = ['red'] * 5

            for col in range(5):
                if guess[col] == target[col]:
                    colors[col] = "green"
                    target[col] = None
            
            for col in range(5):
                if colors[col] == 'green':
                    continue

                if guess[col] in target:
                    colors[col] = "gold"
                    target[target.index(guess[col])] = None

            
            for col in range(5):
                letter = guesses[row][col].upper()
                cell = {"id": f"cell_{row}_{col}", "letter": letter.upper(), "color": colors[col]}
                matrix[row][col] = cell
            status = "Good guess try again"


            
            ## check for the game ending conditions
            if(checkEndGame(guesses[row].upper(), target_text, guesses) == 'win'):
                status = "You Win! Play Again"
                ##disable the button
                guess_button = "disabled"
            if(checkEndGame(guesses[row].upper(), target_text, guesses) == 'lose'):
                status = "You Lose! Game Over"

    context = {"status": status, "matrix": matrix, "target_text":target_text, "old_guesses": guesses, "guess_button": guess_button}
            
    return context

def start_action(request):
    if request.method == 'GET':
        context = {"message": 'Welcome to Wordish'}
        return render(request, 'wordish/index.html', context)
    
    if "target_text" not in request.POST:
        return render(request, 'wordish/index.html', {"message": "Invalid Input"})
    
    try:
        target_text = process_word_parameter(request, "target_text")
        context = compute_game_context(target_text, guesses=[])

        return render(request, 'wordish/game_view.html', context)

    except Exception as e:
        context = {"message": str(e)}
        return render(request, 'wordish/index.html', context)
    

def guess_action(request):
    if request.method == "GET":
        context = {"message": "You're hacking. Try Again!"}
        render(request, 'wordish/index.html', context)
    
    if "target_text" not in request.POST:
        return render(request, 'wordish/index.html', {"message": "Invalid Input"})

    try:
        old_guesses = process_old_guesses(request)
        #print(old_guesses)
        target_text = process_word_parameter(request, "target_text").upper()
    except Exception as e:
        return render(request, 'wordish/index.html', {"message": "Fatal Error:" + str(e)})


    try:
        new_guess = process_word_parameter(request, "guess_text")
        #print("newguess:" + new_guess)
        #print(f"oldguesses: {old_guesses}")
        #old_guesses.append(new_guess)
        context = compute_game_context(target_text, old_guesses + [new_guess])
        #context['status'] = "Good guess try again"
        old_guesses.append(new_guess)
        #print(f"last time oldguesses: {old_guesses}")
        context['old_guesses'] = old_guesses
        

    except Exception as e:
        context = compute_game_context(target_text, old_guesses) #showing the previous guessing still i think
        context['status'] = f"{str(e)}"
        context['old_guesses'] = old_guesses


    return render(request, 'wordish/game_view.html', context)


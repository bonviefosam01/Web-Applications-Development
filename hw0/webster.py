#Problem 1
def join_names(name_list):
    return ",".join(name.strip() for name in name_list)

#Problem 2
def check_name(name):
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if not all (char in letters for char in name):
        raise ValueError("Name must contain letters only.")
    if not(len(name) >= 2 and len(name) <= 11):
        raise ValueError("Name must be between 2 and 11 characters in length")
    vowels = 'AEIOUaeiou'
    if(not any(char in name for char in vowels)):
        raise ValueError("Name must contain at least one vowel")

#Problem 3
def split_names(names):
    lst = [name.strip() for name in names.split(",")]
    [check_name(name) for name in lst]
    return lst

#Problem 4
def my_function_test(f, arg):
    try:
        output = f(arg)
        return("Success: returned value was " + str(output))
    except Exception as e:
        return (f"{type(e).__name__}: {str(e)}")
    
#Problem 5
def my_function_test_2(f, *args, **kwargs):
    try:
        output = f(*args, **kwargs)
        return("Success: returned value was " + str(output))
    except Exception as e:
        return (f"{type(e).__name__}: {str(e)}")
    
#Problem 6
def describe_letters_in_name(name):
    check_name(name)
    lst = [{'position': i, 'letter': char, 'is_vowel': char in 'AEIOUaeiou'} for i, char in enumerate(name)]
    return lst

class Hotel:

    #Problem 7
    def __init__(self, floors, rooms_per_floor):
        if (floors < 1 or rooms_per_floor < 1):
            raise ValueError("Either floors or rooms_per_floor is invalid number (less than 1)")
        else:
            self.floors= floors
            self.rooms_per_floor = rooms_per_floor
            self.matrix = [[{'suite': (f*100 + r),'friend': None,'catch': 0} for r, _ in enumerate(range(self.rooms_per_floor))] for f, _ in enumerate(range(self.floors))]

    #Problem 8
    def get_hotel_matrix(self):
        res =  [[{'suite': self.matrix[i][j]['suite'], 'friend': self.matrix[i][j]['friend'], 'catch': self.matrix[i][j]['catch']} for j in range(len(self.matrix[i]))] for i in range(len(self.matrix))]
        return res
    
    #Problem 9
    def check_in(self, suite_number, name):
        check_name(name)
        f = suite_number // 100
        r = suite_number % 100
        if (suite_number < 0 or r >= self.rooms_per_floor or f >= self.floors):
            raise ValueError(f"Invalid suite number")
        
        if(self.matrix[f][r]['friend'] != None):
            raise HotelError(f"Room {suite_number} is already occupied.")
        
        self.matrix[f][r]['friend'] = name

    #Problem 10
    def catch(self, suite_number):
        f = suite_number // 100
        r = suite_number % 100
        if (suite_number < 0 or r >= self.rooms_per_floor or f >= self.floors):
            raise ValueError(f"Invalid suite number")
        if(self.matrix[f][r]['friend'] == None):
            raise HotelError(f"Room {suite_number} is already vacant.")
            
        self.matrix[f][r]['catch'] += 1
    
    #Problem 11
    def check_out(self, suite_number):
        f = suite_number // 100
        r = suite_number % 100
        if (suite_number < 0 or r >= self.rooms_per_floor or f >= self.floors):
            raise ValueError(f"Invalid suite number")
        if(self.matrix[f][r]['friend'] == None):
            raise HotelError(f"Room {suite_number} is already vacant.")
        
        self.matrix[f][r]['friend'] = None
        self.matrix[f][r]['catch'] = 0
    
    #Problem 12
    def get_room_info(self, suite_number):
        f = suite_number // 100
        r = suite_number % 100
        if (suite_number < 0 or r >= self.rooms_per_floor or f >= self.floors):
            raise ValueError(f"Invalid suite number")
        res = [[{'suite': self.matrix[i][j]['suite'], 'friend': self.matrix[i][j]['friend'], 'catch': self.matrix[i][j]['catch']} for j in range(len(self.matrix[i]))] for i in range(len(self.matrix))]
        return res[f][r]
    
    #Problem 13
    def get_top_rooms(self, k):
        if (k < 0 or k > self.floors*self.rooms_per_floor):
            raise ValueError("The requested number of top rooms cannot exceed thenumber of suites in the hotel.")
        m_copy = [[{'suite': self.matrix[i][j]['suite'], 'friend': self.matrix[i][j]['friend'], 'catch': self.matrix[i][j]['catch']} for j in range(len(self.matrix[i]))] for i in range(len(self.matrix))]
        sorted_rooms = sorted([room for floor in m_copy for room in floor], key = lambda x: x['catch'], reverse=True)
        return sorted_rooms[:k]
    
#Problem 14
class HotelError(Exception):
    def __init__(self, message):
        self.message = message


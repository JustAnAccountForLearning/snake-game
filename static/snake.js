let canvas = document.querySelector('.myCanvas');
let ctx = canvas.getContext('2d');
const BLOCK = 25;
const START_SNAKE_LENGTH = 12;
let NEWGAME = 0;
let SCORE = 0;
drawCanvas();


// Snake Head object
let snek = {
    direction: 'RIGHT',
    newDirection: 'RIGHT',
    length: 6,
    body: [0,250],
    counter: 0,

    set moveHeadX(val) {
        let x = this.body[0][0] + val;
        let y = this.body[0][1];
        if(this.body.length > this.length) { this.body.pop() };
        this.body.unshift([x,y]);
    },
    set moveHeadY(val) {
        let x = this.body[0][0];
        let y = this.body[0][1] + val;
        if(this.body.length > this.length) { this.body.pop() };
        this.body.unshift([x,y]);
    },
    set setDirection(direction) {
        this.counter = 0;
        this.direction = direction;
    }
};

// Food object
let food = {
    x: 200,
    y: 400
};

// Move snake one unit in the direction set
function moveSnake() {
    if (snek.counter == 0) {
        snek.direction = snek.newDirection;
    }
    if (NEWGAME == 0) {
        return;
    }

    // Move the snake in the set direction.
    // Moving a set amount of BLOCK/5 for speed and smoothness
    // based on the increment of 20ms set at the bottom
    switch (snek.direction) {
        case 'UP':
            snek.moveHeadY = -BLOCK/5;
            break;
        case 'DOWN':
            snek.moveHeadY = BLOCK/5;
            break;
        case 'RIGHT':
            snek.moveHeadX = BLOCK/5;
            break;
        case 'LEFT':
            snek.moveHeadX = -BLOCK/5;
            break;
    }

    // Hopefully show the current game score
    document.getElementById("this-score").innerHTML = "YOUR SCORE: " + SCORE.toString();
    
    // Redraw and recheck the screen
    // Order of drawCanvas > drawSnake > dropNewFood > collison retains a very smooth image
    drawCanvas('rgb(0,0,0)');
    drawSnake();
    dropFood();
    collision();
}

function reset() {
    // Set a new location for the food
    foodLocation();
    document.getElementsByTagName("h4")[0].style.visibility = "hidden";

    snek.direction = snek.newDirection = 'RIGHT';
    snek.body = [[0,250]];

    for (i = 0; i < snek.length; i++) {
        snek.body.pop();
    }

    snek.length = START_SNAKE_LENGTH;
    snek.body = setStartBody(START_SNAKE_LENGTH);

    SCORE = 0;
    drawCanvas('rgb(0,0,0)');
    dropFood();
}

// Sets the position of a brand new snake and length
// Uses recursion to cut the tail off the snake.
// I think I really just wanted to practice recursion.
function setStartBody(length) {
    if (length > 1) {
        snek.body.unshift([0,250]);
        length--;
        setStartBody(length);
    }
    return snek.body;
}

// Draw Snake on Canvas
function drawSnake() {
    ctx.fillStyle = 'rgb(0,200,0)';
    for(i = 0, length = snek.body.length; i < length; i++) {
        ctx.fillRect(snek.body[i][0] + 1, snek.body[i][1] + 1, BLOCK - 2, BLOCK - 2);
    }
    snek.counter++;
    if (snek.counter == 5) { snek.counter = 0; }
}

// Tracks snake collision with food, walls, or self
function collision() {
    // Define edges / corners
    let top = snek.body[0][1];
    let right = snek.body[0][0] + BLOCK - 1;
    let left = snek.body[0][0];
    let bottom = snek.body[0][1] + BLOCK - 1;

    // Define colors of the corners
    // T = Top, B = Bottom, R = Right, L = Left
    let TLRed = ctx.getImageData(left + 5, top + 5, 1, 1).data[0];
    let BRRed = ctx.getImageData(right - 5, bottom - 5, 1, 1).data[0];
    let TRRed = ctx.getImageData(right - 5, top + 5, 1, 1).data[0];
    let BLRed = ctx.getImageData(left + 5, bottom - 5, 1, 1).data[0];

    // Snake head corners
    headX = snek.body[0][0];
    headY = snek.body[0][1];

    if (top < 0 || left < 0 || bottom >= canvas.height || right >= canvas.width) 
    { 
        // Sidewall collision
        NEWGAME = 0;
        flashCanvas();
    } 
    else if (TLRed > 100 || BRRed > 100 || TRRed > 100 || BLRed > 100) 
    { 
        // Snake found food
        snek.length += 5;
        foodLocation();
        SCORE += 50;
    }
    else   
    {
        // Snake self collision
        // Need to start at i = 1 so that it doesn't just catch it's head
        for (i = 1; i < snek.length - 3; i++)
        {
            if (headX == snek.body[i][0] && headY == snek.body[i][1])
            {
                NEWGAME = 0;
                flashCanvas();
                break;
            }
        }
        
    } 
}


// The above handles most of the SNAKE functions.
// --------------------------------------------------

function foodLocation() {
    // Randomize within the canvas.
    food.x = Math.ceil((Math.random() * (canvas.width - BLOCK)) / BLOCK) * BLOCK;
    food.y = Math.ceil((Math.random() * (canvas.height - BLOCK)) / BLOCK) * BLOCK;
}

function dropFood() {
    // Ensure the food does not land on the snake body and draw the food.
    for (i = 1; i < snek.length - 3; i++)
    {
        if (food.x == snek.body[i][0] && food.y == snek.body[i][1])
        {
            foodLocation();
        }
    }
    let x = food.x;
    let y = food.y;
    ctx.fillStyle = 'rgb(200,0,0)';
    ctx.fillRect(x, y, BLOCK, BLOCK);
}

// Flash the canvas. Function called upon snake death
function flashCanvas() {
    drawCanvas('rgb(0,0,0)');
    drawSnake();
    dropFood();
    setTimeout(function() {
        drawCanvas('rgb(255,255,255)');
        drawSnake();
        dropFood();
    }, 100);
    setTimeout(function() {
        drawCanvas('rgb(0,0,0)');
        drawSnake();
        dropFood();
    }, 200);
    setTimeout(function() {
        drawCanvas('rgb(255,255,255)');
        drawSnake();
        dropFood();
    }, 300);
    setTimeout(function() {
        drawCanvas('rgb(0,0,0)');
        drawSnake();
        dropFood();
    }, 400);

    setTimeout(function() {
        let form = document.createElement("form");
        form.method = "POST";
        form.action = "highscores";

        let topscore = document.createElement("input");
        topscore.value = SCORE;
        topscore.name = "topscore";
        topscore.id = "topscore";
        form.appendChild(topscore);
        document.body.appendChild(form);

        form.submit();

    }, 1500);
    

}

// Draw Canvas
function drawCanvas(color) {
    var width = canvas.width;
    var height = canvas.height;
    ctx.fillStyle = color;
    ctx.fillRect(0, 0, width, height);
}
// --------------------------------------------------
// Below handles keyboard input for snake game.

// Moves the snake head based on arrow key input
window.addEventListener('keydown', function(event) {
   
    switch (event.keyCode) {
        case 40: // Down
            if (snek.direction != 'UP' && snek.newDirection != 'UP') {
                snek.newDirection = 'DOWN';
            }
            break;
        case 38: // Up
            if (snek.direction != 'DOWN' && snek.newDirection != 'DOWN') {
                snek.newDirection = 'UP';
            }
            break;
        case 37: // Left
            if (snek.direction != 'RIGHT' && snek.newDirection != 'RIGHT') {
                snek.newDirection = 'LEFT';
            }
            break;
        case 39: // Right
            if (snek.direction != 'LEFT' && snek.newDirection != 'LEFT') {
                snek.newDirection = 'RIGHT';
            }
            break;
        case 32: // Spacebar
            NEWGAME = 1;
            reset();
            break;
        default:
            return; // Return nothing when not a valid input.
    }
}, false);

// Time the snake movements
setInterval(moveSnake, 20);

use std::fs;
use std::error::Error;
use regex;

#[derive(Clone, Copy)]
enum Variables {
    W,
    X,
    Y,
    Z,
}

impl Variables {
    fn from_code(s: &str) -> Variables {
        match s {
            "w" => Variables::W,
            "x" => Variables::X,
            "y" => Variables::Y,
            "z" => Variables::Z,
            &_ => panic!()
        }
    }
}

#[derive(Clone, Copy)]
enum Value {
    Variable(Variables),
    Constant(i64)
}

impl Value {
    fn from_code(s: &str) -> Value {
        match s {
            "w" => Value::Variable(Variables::W),
            "x" => Value::Variable(Variables::X),
            "y" => Value::Variable(Variables::Y),
            "z" => Value::Variable(Variables::Z),
            s => match s.parse::<i64>() {
                Ok(number) => Value::Constant(number),
                Err(_) => panic!()
            }
        }
    }
}

#[derive(Clone, Copy)]
enum Instructions {
    Add(Variables, Value),
    Mul(Variables, Value),
    Inp(Variables),
    Eql(Variables, Value),
    Mod(Variables, Value),
    Div(Variables, Value)
}

impl Instructions {
    fn variable(&self) -> &Variables {
        match self {
            Instructions::Add(variable, _) => variable,
            Instructions::Mul(variable, _) => variable,
            Instructions::Inp(variable) => variable,
            Instructions::Div(variable, _) => variable,
            Instructions::Eql(variable, _) => variable,
            Instructions::Mod(variable, _) => variable
        }
    }
}

struct Program {
    instructions: Vec<Instructions>
}

impl Program {
    fn from_string(string: String) -> Program {
        let lines = string.lines();

        let re = regex::Regex::new(r"(\w\w\w) (x|y|z|w) ?(x|y|z|w|(-?\d*))?").unwrap();

        let instructions = lines.map(|line| {
            let capture = re.captures(line).unwrap();
            let op_code = &capture[1];
            match op_code {
                "add" => Instructions::Add(Variables::from_code(&capture[2]), Value::from_code(&capture[3])),
                "inp" => Instructions::Inp(Variables::from_code(&capture[2])),
                "mul" => Instructions::Mul(Variables::from_code(&capture[2]), Value::from_code(&capture[3])),
                "mod" => Instructions::Mod(Variables::from_code(&capture[2]), Value::from_code(&capture[3])),
                "div" => Instructions::Div(Variables::from_code(&capture[2]), Value::from_code(&capture[3])),
                "eql" => Instructions::Eql(Variables::from_code(&capture[2]), Value::from_code(&capture[3])),
                &_ => panic!()
            }
        }).collect();

        Program {
            instructions
        }
    }
}

#[derive(Clone, Copy)]
struct Environment<'a> {
    program: &'a Program,
    w: i64,
    x: i64,
    y: i64,
    z: i64,
    input: Option<i64>,
    start: usize
}

impl<'a> Environment<'a> {
    fn from_program(program: &'a Program) -> Environment<'a> {
        Environment {
            program,
            w: 0,
            x: 0,
            y: 0,
            z: 0,
            input: None,
            start: 0
        }
    }

    fn input(&mut self, input: i64) {
        self.input = Some(input);
    }

    fn run(&mut self) {
        for i in self.start..self.program.instructions.len() {
            let instruction = self.program.instructions[i];
            let result = match instruction {
                Instructions::Mul(variable, value) => self.number_from_variable(&variable) * self.number_from_value(&value),
                Instructions::Add(variable, value) => self.number_from_variable(&variable) + self.number_from_value(&value),
                Instructions::Inp(_) => match self.input {
                    Some(number) => {
                        self.input = None;
                        number
                    },
                    None => {
                        self.start = i;
                        break
                    }
                },
                Instructions::Eql(variable, value) => if self.number_from_variable(&variable) == self.number_from_value(&value) {
                    1
                } else {
                    0
                },
                Instructions::Mod(variable, value) => self.number_from_variable(&variable) % self.number_from_value(&value),
                Instructions::Div(variable, value) => self.number_from_variable(&variable) / self.number_from_value(&value) // Floor division because of i64
            };

            self.set_variable(instruction.variable(), result);
        }
    }

    fn number_from_value(&self, value: &Value) -> i64 {
        match value {
            Value::Constant(number) => number.clone(),
            Value::Variable(variable) => self.number_from_variable(variable)
        }
    }

    fn number_from_variable(&self, variable: &Variables) -> i64 {
        match variable {
            Variables::W => self.w,
            Variables::X => self.x,
            Variables::Y => self.y,
            Variables::Z => self.z
        }
    }

    fn set_variable(&mut self, variable: &Variables, number: i64) {
        match variable {
            Variables::W => self.w = number,
            Variables::X => self.x = number,
            Variables::Y => self.y = number,
            Variables::Z => self.z = number
        }
    }
}

fn main() -> Result<(), Box<dyn Error>> {
    // Parse input
    let input = fs::read_to_string("../input.txt")?;

    // Get the program and env
    let program = Program::from_string(input);

    let mut env = Environment::from_program(&program);

    env.input(9);
    // Runs until the second input token
    env.run();

    Ok(())
}

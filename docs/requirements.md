# Tibber Technical Case 

Create a new microservice that could fit into the Tibber Platform environment as described above. 

The created service will simulate a robot moving in an office space and will be cleaning the places this robot visits. 

The path of the robot's movement is described by the starting coordinates and move commands. 

After the cleaning has been done, the robot reports the number of unique places cleaned. The service will store the results into the database and return the created record in JSON format. 

The resulting value will be stored in a table named `executions` together with a timestamp of insertion, number of command elements and duration of the calculation in seconds.

Stored record example:

|  ID  | Timestamp                  | Commands | Result | Duration | 
|:----:|:---------------------------|:--------:|:------:|:--------:|
| 1234 | 2018-05-12 12:45:10.851596 |    2     |   4    | 0.000123 |


The service listens to HTTP protocol on port 5000. 

## API Request: 
- Method: POST 
- Request path: /tibber-developer-test/enter-path 
- Input criteria: 
  - 0 ≤ number of `commmands` elements ≤ 10000 
  - −100 000 ≤ `x` ≤ 100 000, x ∈ Z 
  - −100 000 ≤ `y` ≤ 100 000, y ∈ Z 
  - `direction` ∈ {north, east, south, west} 
  - 0 < `steps` < 100000, steps ∈ Z 

### Request body example: 

```json
{
  "start": {
    "x": 10,
    "y": 22
  },
  "commmands": [
    {
      "direction": "east",
      "steps": 2
    },
    {
      "direction": "north",
      "steps": 1
    }
  ]
}
```

### Response body example:

```json
{
    "id": 2,
    "commands": 2,
    "result": 4,
    "duration": 0.00024289700377266854,
    "timestamp": "2023-11-06T10:52:15.202460Z"
}
```

## Notes 

You can assume, for the sake of simplicity, that:

- The office can be viewed as a grid where the robot moves only on the vertices.
- The robot cleans at every vertex it touches, not just where it stops. 
- All input should be considered well formed and syntactically correct. There is no need, therefore, to implement elaborate input validation. 
- The robot will never be sent outside the bounds of the office. 
- Ensure that database connection is configurable using environment variable. 
- Think about structure, readability, maintainability, performance, re-usability and test-ability of the code. Like the solution is going to be deployed into the production environment. You should be proud of what you deliver. 
- Use only open source dependencies if needed. 
- Include Dockerfile and docker-compose configuration fi les in the solution.

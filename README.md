# Agent-based Model

## Install

In the Client and Server directories, run `pip install -r requirements.txt` to install the required packages.

## Run

### Server

Requires Python 3.9 or later for running prediction requests on another thread. Runs on port **8000**.

In the Server directory, run `python Main.py <CONFIGURATION_PATH>` to start the server, e.g. `python Main.py Configuration/store1.json`.

#### Clearing output

To clear the Output folder at the start of running the server, add the CLEAR_OUTPUT environment variable, e.g. `CLEAR_OUTPUT=1 python Main.py Configuration/store1.json`.

#### Predictions

If there is at least one item in the store, the server will send a request to the prediction API at each time step with the state of each item in the store. The most recent prediction for each item will be visible in the client.

The prediction API is assumed to run on port **8080** (this can be changed for Uvicorn by adding `UVICORN_PORT=8080 ` before your command to run). The prediction API should be able to handle POST requests to `/predict` with a JSON body containing the state of each item in the store.

### Client

You should ensure the server is running before starting any clients.

#### One random agent

In the Client directory, run `python Main.py`. This will randomly configure either a shopper agent or a shoplifter agent to pick up a random number of items.

#### One configured agent

In the Client directory, run `python Main.py <AGENT_CONFIGURATION_PATH>`. This will configure the agent according to the specified JSON file. e.g. `python Main.py Configuration/Shopper1.json`.

#### Multiple agents

In the Client directory, run `python Spawner.py`. This will run batches of agents with random configurations up to the total number of specified players.

The recommended batch size is 10. Remember to adjust the minimum number of players in `Server/Game/Game.py` if you wish for them all to start moving at the same time.

#### Spectator

In the Client directory, run `GRAPHICS_MODE=1 python Spectator.py`. This will run a spectator mode where you can watch the agents move around the store. You will not be able to control any agents.

#### Controller

In the Client directory, run `GRAPHICS_MODE=1 python Controller.py <AGENT_TYPE>`. e.g. `GRAPHICS_MODE=1 python Controller.py SHOPPER`.

This will run a controller mode where you can control a single agent with the arrow keys. The agent type can be either SHOPPER or SHOPLIFTER.

It is important to set the correct agent type if you are controlling an agent to create a human dataset, otherwise the items that you pick up will not be labelled as being picked up by a shoplifter.

If you are controlling a shopper for validating a machine learning model in real-time (and NOT using the saved data), you can default to SHOPPER.

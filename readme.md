#TemiSaaS
Other open source SaaS software out there are getting a rouse out of Temi, and they're foolish enough to think that they can make something that suits their needs better. Heavily inspired by Piku

#### What is Temi's needs?

Temi demands of the following features out of their new created SaaS:

- Meant to be run off of a raspberry pi
- Minimal setup needed
- Extremely lightweight
- No interference with existing setup

#### What does the progress look like right now?
Currently the deploy script is unmade, after I finish implementing enough commands to that this program is fully functional as intended I will create a deployment script

Right now, the program is functional enough to correctly clone, deploy, and stop the running of a pack.

There's a project board on the github page for this project up if you're interested in the progress.

#### What's good about it? (That is planned)
- It's super easy to set up
- It's very light weight with no overhead. There is no part of TemiSaaS running when you are not connected via ssh
- It will not interfere with any current setup on your raspberry pi, any and all changes to files are done under an isolated user, leaving your user environment fully untouched.
- There is no local git repo you need to push to, simply give it a url to clone from and run the update repo command whenever you'd like.
- Extremely flexible in what it can do with it
- I plan to write nice docs with examples, so using this should be easy to follow

#### What's bad about it?
- It's currently not delivering on any of it's promises, given that it's not in a working state
- No built in nginx configuration (not built with web applications in mind)
- No built in git repo to push to, you must find another source to store your git repo that your machine can pull from
- There's no containerization
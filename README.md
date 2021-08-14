# · Employee System App With Login/Register
A CRUD with login and registration included (The security and authentication is a bit simple, but for a quick "project" it's not bad) There may be bugs that I missed, or that the authentication could be improved; I did this project because I had nothing to do during the weekend, and partly because I saw a video that inspired me to do it and add a login. The code is a bit messy and it's easy to get lost, but as I say, it's not a "complete" project where I upload it to a server and etc..... 

# ~ About the application ~
It tries to manage employees, either add, delete or edit one; the login and registration I added it to make it almost complete. (I know I may be missing many things, what I will do in my spare time is to improve this application until it is complete) I will show some images so you can see how it is.

# ~ Project Image ~
![alt text](https://i.imgur.com/sex7Axi.png)

![alt text](https://i.imgur.com/XnUyrsh.png)

![alt text](https://i.imgur.com/qbN9dly.png)

![alt text](https://i.imgur.com/xOzzcD0.png)

# ~ Additional information ~

In the images shown above, you can see an "edit" and a "delete"; as the name says, the edit has the function to edit an employee (name, email and photo); and the "delete" deletes the employee, but before it launches a confirmation created in JavaScript if you press "Ok" it is deleted, but if you select "cancel" the item is not deleted. And the "logout" that appears in the corner next to the user's name closes the session that was active at that moment. Once logged in/registered you can't go back to "/login" or "/register"; basically if you are already inside the application with the active session you can't go from "/home" -> "/login"; to go back to "/login" you must press the "exit" button which closes the session.

Once the session is closed you can not access the home page, you can not delete or edit, or through the url you can not, if you try to enter for example "/edit/17" automatically redirects you to "/login" to log in or register.  Nor can you delete it, if you try to access for example "/delete/17" you will not be able to because it will redirect you to the "/login" page or if you do not have any account you can register in "/register".

# ~ End ~

I may not have explained the application, login and CRUD in general very well or in depth, but I have tried to do my best, and sorry if the code looks too verbose, when I have free time I will take it apart and improve it little by little. I have several codes that I haven't uploaded because some I use for work and I can't publish them, (Others I don't upload because they are mostly pretty simple CRUD that I made in languages like php, java, python and JavaScript mostly.) but I will try to publish the codes of the applications that I make in my free time (Like this one). Possibly I will upload the others, although I don't know haha, I'll see what I do.

# Greetings and goodbye <3
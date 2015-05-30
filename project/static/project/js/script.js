

function populateNavBar(sname, urlCreateProject, urlSignUp, urlLogin, urlLogout, urlAccountSettings, urlSavedProjects, urlMyProjects, urlFabCreate)
{
	if (sname.length>0)
	{
		element1 = document.getElementById('navid1');
		element1.innerHTML = "Create Project";
		element1.href = urlCreateProject;
		element2 = document.getElementById('navid2');
		element2.innerHTML = "Saved Projects";
		element2.href = urlSavedProjects;
		element3 = document.getElementById('navid3');
		element3.innerHTML = "My Projects";
		element3.href = urlMyProjects;
		element4 = document.getElementById('navid4');
		element4.innerHTML = "Fabricator";
		element4.href = urlFabCreate;
		element5 = document.getElementById('navid5');
		element5.innerHTML = "Account Settings";
		element5.href = urlAccountSettings;
		element6 = document.getElementById('navid6');
		element6.innerHTML = "Log Out";
		element6.href = urlLogout;
		element = document.getElementById('navidSignUp');
		element.style.visibility = "hidden";
	}else{
		element1 = document.getElementById('navid1');
		element1.style.visibility = "hidden";
		element2 = document.getElementById('navid2');
		element2.style.visibility = "hidden";
		element3 = document.getElementById('navid3');
		element3.style.visibility = "hidden";
		element4 = document.getElementById('navid4');
		element4.style.visibility = "hidden";
		element5 = document.getElementById('navid5');
		element5.style.visibility = "hidden";
		element6 = document.getElementById('navid6');
		element6.innerHTML = "Log In";
		element6.href = urlLogin;
		element = document.getElementById('navidSignUp');
		element.innerHTML = "Sign Up";
		element.href = urlSignUp;
	};
};

function printdate()
{
	test = new Date();
	month = test.getMonth();
	month = (month * 1) + 1;
	day = test.getDate();
	year = test.getFullYear();
	window.alert(" ",month,"/",day,"/",year," ");
};
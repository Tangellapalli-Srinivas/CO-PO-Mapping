# CO-PO Mapping

Flexible computational tool for the Outcome based Education

## Introduction

* Currently, outcome-based education (OBE) is getting more attention in engineering institutes for continuous improvement of the quality of the teaching-learning process. 

* Evaluation and analysis of the attainment of course outcomes (COs) and programme outcomes (POs) through mapping (correlation) helps to manage the quality loop. 

* From this practice, faculty can review the progress made by the student’s performance and the stakeholder’s inputs for better job performance and achieve the desired outcomes. 
But the mapping process for CO attainment is complex in nature, and it needs more time for execution. 

* To assist the faculty with their busy schedules, a fast, generalized, and automated tool has been developed for CO-PO mapping and attainment evaluation and analysis. 

* This is suitable for open and distance learning education due to the paperless assessment. 

* Through this exercise, faculty can supply the actual obtained students' marks to the tool/app and generate the results for the attainment analysis.

* It saves the faculty burden and allows quick decisions on the quality improvement process.

* The procedure is generalised with the number of exams, number of COs, multiple COs tagged to a single question, number of PSOs, number of questions and weightage in marks.




## Pre-Requisite
 
* Matlab R2018a / R2018b / R2019a / R2019b R2020a / R2020b
* Runs on Windows only


## Process

1. Start the Application
2. Check if the Latest release of this application is in beta that is `v0.0.*`. **(So needs internet just for starting this application)**
3. Loads the Matlab engine (Shows Loading Page) (Application is in `locked` state)
4. After Loading, Moves to main Page (Matlab Engine is in `idle` state)
5. Submits data
6. Matlab Processes the given data (Application is now in `locked` state)
7. Matlab Engine after processing, returns the results accordingly (Matlab Engine is in `idle` state)
8. Application waits for User to submit the data

* <u>`Idle`</u>

    When the Matlab Engine is in idle state, we can submit the data and ask engine to process it

* <u>`Locked`</u>
    
    When the Application is in locked state, then we cannot submit another set of input, instead we need to wait until it is done processing or loading.

## Header

Regardless of whatever state the Application or Engine is in, we can use this five elements which are at the header.

* Auto - Update  
  
    Toggle for checking update everytime it needs

* [Github Issue Link](https://github.com/Tangellapalli-Srinivas/CO-PO-Mapping/issues)

    You can report any issue you face in this application [here](https://github.com/Tangellapalli-Srinivas/CO-PO-Mapping/issues)

* Shutting down the Engine

    Recommended way to Shut down the Application. It will first check for the updates if auto-update was turned on and then shuts down the application.

* Status Check
  
    It is sometimes possible for your application not in sync with the main process. Just click on this, to refresh if needed if already in sync, it notifies you the status
    
* Restart the Engine

    Starts your application from step-2 from the steps mentioned [here](#process). Note whatever task was assigned to Engine will be lost.
    
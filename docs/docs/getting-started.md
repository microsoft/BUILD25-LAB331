# Getting Started

## **Microsoft Build Attendees**

The instructions on this page assume you are attending [Microsoft Build 2025](https://build.microsoft.com/){:target="_blank"} and have access to a pre-configured lab environment. This environment provides an Azure subscription with all the tools and resources needed to complete the workshop.

## **Introduction**

This workshop is designed to teach you how to use Reasoning Models, like DeepSeek R1 and utilize tools and Reflection style architecture with LangChain to do deep research. It consists of multiple labs, each highlighting a specific feature of the process of building a deep researcher. The labs are meant to be completed in order, as each one builds on the knowledge and work from the previous lab.

## **Authenticate with Azure**

You need to authenticate with Azure to access DeepSeek R1. Follow these steps:

1. Open a terminal window. The terminal app is **pinned** to the Windows taskbar.

    ![Open the terminal window](../media/windows-taskbar.png){ width="300" }

2. Run the following command to authenticate with Azure:

    ```powershell
    az login
    ```

    !!! note
        You'll be prompted to open a browser link and log in to your Azure account.

        1. A browser window will open automatically, select **Work or school account** and click **Next**.

        1. Use the **Username** and **Password** found in the **top section** of the **Resources** tab in the lab environment.

        2. Select **OK**, then **Done**.

3. Then select the **Default** subscription from the command line.

4. Stay in the terminal window for the next step.

## **Open the Workshop and setup your Tavily account**

Follow these steps to open the workshop in Visual Studio Code and set up your Tavily account for web search:


1. From the terminal window, execute the following commands to clone the workshop repository, navigate to the relevant folder, set up a virtual environment, activate it, and install the required packages:

    ```powershell
    git clone https://github.com/microsoft/BUILD25-LAB331.git `
    ; cd BUILD25-LAB331 `
    ; python -m venv src/.venv `
    ; src\.venv\Scripts\activate `
    ; pip install -r src/requirements.txt `
    ; cd src `
    ;
    ```

    This command will take a few minutes to complete. While you wait, navigate to the Tavily home page that should already be opened as a tab in your browser. 


2. We will be using [Tavily](https://tavily.com/) to give our deep researcher access to the internet. Once on the Tavily page, click the sign up button and create an account. 

    !!! note
        You will need to use either your personal email address or your Github account to sign up since email requires verification. 


    Click the signup button and complete the sign up process 

    ![click the signup button](../media/tavily-signup.jpg){ width="800" }

    Once sign up is complete you should see a page with an API Key that looks like this. You will use this key later, so minimize the page for now and return to the terminal. 

    ![click the signup button](../media/tavily-api-page.png){ width="800" }


3. From the terminal window, run the following command to open the project in VS Code (note there is a period after the word code. Do not just type in 'code', the period is important.):

    ```powershell
    code .
    ```

    !!! warning "When the project opens in VS Code, two notifications appear in the bottom right corner. Click ✖ to close both notifications."


## **Configure the Workshop**

### **Create the .env file**

1. Open a new terminal in VSCode. 

2. To create a `.env` file with the variables needed for this workshop click on the `instructions` tab in your Skillable lab manual. Click on the command under Lab Guide and patse it in the terminal. Press enter to run the command and follow the instructions.
3. Check that your .env file has succesfully been created and contains some variables. If not, raise your hand and ask a proctor for help.
4. Navigate back to the Tavily API page you should have open in your browser. Copy the API Key and paste it in the .env file as the `TAVILY_API_KEY` value.

You can now begin with Lab 1! 

## **Navigation**

Use the navigation menu on the left to move between labs.

## **Pro Tips**

!!! tips
    1. The **Burger Menu** in the right-hand panel of the lab environment offers additional features, including the **Split Window View** and the option to end the lab. The **Split Window View** allows you to maximize the lab environment to full screen, optimizing screen space. The lab's **Instructions** and **Resources** panel will open in a separate window.
    2. If the lab instructions are slow to scroll in the lab environment, try copying the instructions’ URL and opening it in **your computer’s local browser** for a smoother experience.
    3. If you have trouble viewing an image, simply **click the image to enlarge it**.

## **Next Steps**

Once your environment is set up, proceed to [Lab 1: Reasoning & Model Thoughts](lab-1-reasoning-thoughts.md) to begin building your research assistant.

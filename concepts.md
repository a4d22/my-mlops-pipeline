Docker VOlumes

Think of Docker containers as temporary hotel rooms. You can stay there, mix things up, and turn on the TV, but the moment you check out (delete the container), anything you left in the fridge is gone forever.Docker Volumes are the solution to this. They act like a permanent storage locker down the hall. No matter how many times you check in or out of the hotel, your stuff stays safe, intact, and right where you left it.Here is a breakdown of how volumes work in Docker Compose, the syntax, and the different approaches you can take.1. The Core ConceptBy default, data created inside a container lives on a temporary writable layer. If the container is deleted, the data dies with it.Volumes decouple the lifecycle of the data from the lifecycle of the container. They allow you to:Persist data: Keep database records, user uploads, or logs safe when containers restart or upgrade.Share data: Allow multiple containers to access and modify the same files simultaneously.Mount host files: Sync code from your local machine into the container for real-time development.2. The Two Main ApproachesWhen working with Docker Compose, you will generally choose between Named Volumes and Bind Mounts.Approach A: Named Volumes (Managed by Docker)Docker creates and manages a dedicated folder on your host machine's hard drive (usually deep inside /var/lib/docker/). You don't need to worry about the exact path; Docker handles it securely.Best for: Databases (MySQL, PostgreSQL), persistent application data, and production environments.Pros: High performance, isolated from host system messiness, easy to back up via Docker.Approach B: Bind Mounts (Managed by You)You map a specific, explicit path on your host machine (like ~/Projects/my-website) directly into the container.Best for: Live development (hot-reloading code) and sharing configuration files (like an nginx.conf).Pros: Any change you make in your local code editor instantly reflects inside the running container.3. Syntax in Docker ComposeDocker Compose uses a volumes: key. Depending on the approach, the syntax changes slightly.The Short Syntax (HOST:CONTAINER)The most common way to write volumes is the short syntax, which follows the pattern: [source]:[destination]:[ro/rw]Here is a complete docker-compose.yml example demonstrating both approaches:YAMLversion: '3.8'

services:
  web_app:
    image: node:18
    ports:
      - "3000:3000"
    # APPROACH B: Bind Mount (Local code syncing)
    volumes:
      - .:/app # Maps current directory (.) on host to /app inside container
      - /app/node_modules # Anonymous volume (prevents host from overwriting container node_modules)

  database:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: secretpassword
    # APPROACH A: Named Volume (Data persistence)
    volumes:
      - db_data:/var/lib/postgresql/data # Named volume mapped to Postgres data dir

# Crucial step: Named volumes MUST be declared in a top-level volumes key
volumes:
  db_data:
The Long Syntax (More Explicit)If you want to be incredibly clear or need to pass specific options (like read-only permissions), you can use the long syntax:YAMLservices:
  web_app:
    image: nginx:latest
    volumes:
      - type: bind
        source: ./nginx.conf
        target: /etc/nginx/nginx.conf
        read_only: true # Prevents the container from altering your host config file
Cheat Sheet: Quick ComparisonFeatureNamed Volumes (db_data:/path)Bind Mounts (./local/path:/path)Storage LocationManaged by Docker (/var/lib/docker/...)Anywhere you choose on your host machinePrimary Use CaseDatabases, Production state, CacheSource code editing, Config sharingHost DependencyIndependent of host OS file structureHighly dependent on host file pathsPerformanceExcellent (especially on macOS/Windows)Can be slower on macOS/Windows due to OS syncingInitializationPopulates new volume with container dataOverwrites container data with host data




REGRESSION Testing
--------------------

Imagine you live in a house and decide to remodel the kitchen. The contractors come in, do a fantastic job, and install beautiful new cabinets. But when they leave, you go to turn on the bathroom shower, and suddenly only freezing cold water comes out.The contractors fixed one thing, but accidentally broke something else that used to work perfectly.In computer science, that "broken shower" is called a regression. Regression testing is the practice of testing your existing software after changes have been made to ensure that the old features still work exactly as they did before.1. Why Do We Need It?Codebases are deeply interconnected networks. A tiny, well-intentioned tweak to a checkout page button could accidentally corrupt the database logic responsible for sending email receipts.Whenever a developer:Adds a new featureFixes a bugOptimizes code for performanceUpdates a dependency or library...they risk introducing a regression. Regression testing acts as a safety net, catching these unintended side effects before the software reaches real users.2. Types of Regression TestingDepending on how much time you have and how massive the code changes are, teams choose different strategies:Re-test All: The most thorough approach. You rerun every single test case in your entire library. It’s highly secure but incredibly time-consuming and expensive.Selective Regression: You only test the parts of the software that are directly or indirectly related to the code that was changed. If you modified the "Payment Gateway," you test checkout and user profiles, but skip the "Dark Mode" toggle settings.Progressive Regression: Used when the system architecture itself has changed significantly, requiring new test cases to be written alongside the old ones.3. How It Is Done (Automation is Key)In the early days of software, human QA testers had to manually click through every single button of an app after every update. Today, manual regression testing is mostly dead because it doesn't scale.Instead, teams use Automated Testing.The Suite: Developers maintain a "test suite" (a massive collection of code scripts designed to test the app).The Trigger: Whenever a developer pushes new code, a CI/CD pipeline (Continuous Integration/Continuous Deployment) automatically runs the entire test suite in the background.The Result: If a single old test fails, the build turns "red," alerting the developer immediately that they broke an existing feature.The Difference: Regression vs. Re-TestingThese two terms are often confused, but they mean different things:FeatureRe-TestingRegression TestingPurposeTo confirm a specific bug was actually fixed.To confirm that a fix didn't break other things.FocusDefect-centric (testing the exact spot of the error).System-centric (testing the health of the whole app).ExecutionDone immediately after a bug fix.Done after the bug fix passes re-testing.

-- This represents Regression Testing. As systems scale, developers modify old functions to add new features. A regression occurs when a new change inadvertently breaks an existing, verified feature.


365627072460.dkr.ecr.us-east-1.amazonaws.com/housing-predict-service


4. Workflow

AWS_TOKEN=$(aws ecr get-login-password --region us-east-1)
winpty docker login --username AWS --password $AWS_TOKEN 365627072460.dkr.ecr.us-east-1.amazonaws.com

To push any local image to AWS, you must always follow this 3-step structural dance:

[1. Authenticate CLI] ──► Requests temporary 12-hour Docker token from AWS
            │
            ▼
[2. Tag Local Image]  ──► Creates an alias pointing to the remote AWS URI
            │
            ▼
[3. Docker Push]      ──► Uploads layers to Amazon ECR Repository



----------------

To connect our cloud server safely to the public internet, we must master three fundamental cloud networking concepts:

AMI (Amazon Machine Image): The operating system blueprint. We will use a standard, stable Ubuntu Linux image.

Instance Type: The hardware profile. We will use t3.micro or t2.micro (depending on availability), which fall completely under the AWS Free Tier (750 free hours per month).

Security Group: A virtual firewall that controls inbound and outbound traffic. By default, EC2 blocks all traffic. We must explicitly open ports to access it:

Port 22 (SSH): To securely log in and configure the server from our terminal.

Port 80 (HTTP): To allow public users and web browsers to send data to our FastAPI app.


Step 1: Create an SSH Key Pair
This generates a cryptographic key file (mlops-key.pem) that acts as the absolute password to access your server.

Bash
aws ec2 create-key-pair \
    --key-name mlops-key \
    --query 'KeyMaterial' \
    --output text > mlops-key.pem
CRITICAL Security Step for Mac/Linux users (Skip if on standard Windows CMD): You must restrict file permissions so AWS allows you to use it:


Step 2: Create a Firewall (Security Group)
Create a security group named mlops-sg and capture the Group ID from the output:

Bash
aws ec2 create-security-group \
    --group-name mlops-sg \
    --description "Security Group for MLOps FastAPI Server"
(Look at the output JSON and note your "GroupId", which looks like sg-0abc123456789def0)

"GroupId": "sg-05147500e90fb6286",


Step 3: Add Open Port Rules to the Firewall
Authorize Port 22 (for your keyboard access) and Port 80 (for global API traffic). Replace sg-xxxxxx with your actual Group ID from the previous step:

Bash
# Allow SSH access from anywhere
aws ec2 authorize-security-group-ingress --group-id sg-xxxxxx --protocol tcp --port 22 --cidr 0.0.0.0/0

# Allow HTTP web traffic from anywhere
aws ec2 authorize-security-group-ingress --group-id sg-xxxxxx --protocol tcp --port 80 --cidr 0.0.0.0/0
Step 4: Launch the EC2 Instance Server
Now we fire up the server! We will use the standard Ubuntu 24.04 LTS AMI. Run this command (make sure to update your Security Group ID):

Bash
aws ec2 run-instances \
    --image-id ami-04b70fa74e45c3917 \
    --count 1 \
    --instance-type t3.micro \
    --key-name mlops-key \
    --security-group-ids sg-xxxxxx
(Note: ami-04b70fa74e45c3917 is the official standard Ubuntu 24.04 image for us-east-1. If you configured your AWS CLI to a different region like ap-south-1 (Mumbai), use ami-090fa75e783edd897 instead).


Find your Server's Public IP Address:
Run this command to check your running instances:

Bash
aws ec2 describe-instances --query "Reservations[*].Instances[*].[InstanceId, PublicIpAddress, State.Name]" --output table
Locate your running instance and copy its PublicIpAddress (e.g., 54.210.23.144).

SSH into your cloud server:
Using the key pair generated in Step 1, run the following command in the terminal directory where mlops-key.pem is saved:

Bash
ssh -i mlops-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
Type yes when prompted to confirm the connection security fingerprint. You are now officially commanding a terminal operating directly inside AWS's cloud data center!

Install Docker inside the EC2 Server:
While logged into your EC2 instance terminal prompt (ubuntu@ip-xx-xx-xx-xx:$), copy-paste this standard script block to clear old software libraries and install a clean Docker runtime engine:

Bash
sudo apt-get update -y
sudo apt-get install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker
# Allow the ubuntu user to run docker commands without typing sudo every time
sudo usermod -aG docker ubuntu
Verify the server installation:
Log out of the server and log back in to apply the group changes, then type:

Bash
docker --version
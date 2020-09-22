# Download All Links
A simple utility to download all contents or images from a web page (URL or local file)

# Usage
`python main.py --url {URL_OR_PATH} --tag {TAG} --prefix {PREFIX} --suffix {SUFFIX}`

Arguments    

**--url** specify URL to a webpage or path to a local file    
**--tag** what HTML tag to download (e.g. 'a' for downloadable links,  'img' for image links)    
**--prefix** (optional) specify the prefix schema of downloadable links (e.g. 'https://s3', 'ftp://')     
**--suffix** (optional) specify the suffix schema of downloadable contents (e.g. '.zip', '.png', '.jpg', '.tar')    


# Example
Download all images from Wikipedia landing page:     
`python main.py --url https://en.wikipedia.org/wiki/Main_Page --tag img`

Download all zip archites contained in https links from a local HTML page:      
`python main.py --url path_to_html_file --tag a --prefix https:// --suffix .zip`


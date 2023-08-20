from distutils.core import setup
setup(
  name = 'vessel_BalticShipping',         
  packages = ['vessel_BalticShipping'],   
  version = '1.12',      
  license='GNU Affero General Public License v3.0', 
  description = 'Obtain Ship/ vessel data based on imo number',   
  author = 'Abhishek Venkatachalam',              
  author_email = 'abhishek.venkatachalam06@gmail.com',  
  url = 'https://www.linkedin.com/in/abhishek-venkatachalam-62121049/',
  # download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['Ship data', 'imo', 'vessel data', 'vessel imo gross tonnage data'], 
  install_requires=[
          'requests',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)', 
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
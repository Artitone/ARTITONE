# ARTITONE

[![Python Version](https://img.shields.io/badge/python-3.7-brightgreen.svg)](https://python.org)
[![Django Version](https://img.shields.io/badge/django-3.2.8-brightgreen.svg)](https://djangoproject.com)
[![Coverage Status](https://coveralls.io/repos/github/Artitone/ARTITONE/badge.svg?t=0UBQcT)](https://coveralls.io/github/Artitone/ARTITONE)
[![Continuous Integration](https://github.com/Artitone/ARTITONE/actions/workflows/presubmit.yml/badge.svg?branch=main)](https://github.com/Artitone/ARTITONE/actions/workflows/presubmit.yml)
[![Continuous Deployment](https://github.com/Artitone/ARTITONE/actions/workflows/merge_deploy.yml/badge.svg?branch=main)](https://github.com/Artitone/ARTITONE/actions/workflows/merge_deploy.yml)

## Topology
### 1. Artist Models
- **Artist**
  - First Name(Not a must)
  - Last Name(Not a must)
  - Nickname(pk)
  - Paycheck Method
  - Artworks
 
- **Artwork**
  - Name
  - Price
  - Photo(at least one)
  - _Texture_(Auto-detect)
  - _Category_(Auto-detect)
  - Description

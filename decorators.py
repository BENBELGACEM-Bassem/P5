# coding: utf-8
"""This module is responsible for defining needed decorators for th project """

from functools import wraps


def run_once(f):
	"""This function ensures that a given function is run only once"""
	@wraps(f)
	def wrapper(*args, **kwargs):
		if not wrapper.has_run:
			wrapper.has_run = True
			return f(*args, **kwargs)
	wrapper.has_run = False
	return wrapper

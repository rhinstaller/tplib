.. _file_structure:

==============
File structure
==============

There's no filesystem organization structure where test plans, requirements and
test cases are discovered by :py:class:`testcases.library.Library`. All the
structures should be then accessed through the
:py:class:`testcases.library.Library` object.

Structures are destinguished by their filename suffix (described below) and
are available in :py:class:`testcases.library.Library` after successful load.
If a file doesn't contain correct structure, there will be error raised during
discovery.

Test plan (currently not implemented)
=====================================

:suffix: ``.plan.yaml``
:class: :py:class:`testcases.structures.testplan.TestPlan`
:library attribute: ``testplans``
:yaml structure (TBD):

.. _requirement_structure:

Requirement
===========

:suffix: ``.req.yaml``
:class: :py:class:`testcases.structures.requirement.Requirement`
:library attribute: ``requirements``
:yaml structure:

   * **name** (`str`, `unique`) --
   * **description** (`str`) --
   * **tags** (`list`) --
   * **verified_by** (`dict` - :py:class:`testcases.structures.requirement.AcceptanceCriteria`)

     :one of:
      * **direct_list** (`list`) -- List of testcases names
      * **query** (`str`) -- Jinja2 expression, see more here: TBD

   * **acceptance_criteria** (`dict`) --

Examples
--------

.. literalinclude:: ../../tests/scenarios/removed_testcase/old/direct.req.yaml
   :language: yaml

.. literalinclude:: ../../tests/scenarios/removed_testcase/old/priority.req.yaml
   :language: yaml

.. _testcase_structure:

Test case
=========
:suffix: ``.tc.yaml``
:class: :py:class:`testcases.structures.testcase.TestCase`
:library attribute: ``testcases``
:yaml structure:

 * **name** (`str`, `unique`) -- Test case name used as identifier inside
   library
 * **description** (`str`) -- TODO
 * **priority** (`int`) -- This can be theoretically any number. Convention
   is to use values in range <1,10> where higher number means higher priority.
 * **execution** (`dict`) --

   * **type** (`str`) -- This field is used by automation of testcase
     execution (pipeline) where the value signals what kind of execution is
     used for this test case. Special word `manual` is used to signal that
     manual (human) execution is required and no automation is available.
     The `manual` word is also interpreted when the testcase is exported e.g.
     to Polarion.
   * **automation_data** (any type, optional) -- The data type depends on the
     automation of testcase execution (pipeline) and can be used as
     machine-readable execution instructions. This field can be used even
     in case of `manual` for purposes of some upcoming automation.

 * **filter** (`list`, `optional`) -- TBD
 * **instructions** (`dict` - :py:class:`testcases.structures.testcase.Instructions`)

   * **setup** (`list`, `optional`) -- list of :py:class:`testcases.structures.testcase.Instruction`

     :variable item (full):
      * **step** (`str`) --
      * **result** (`str`, `optional`) -- (default: 'Success')

     :variable item (short):
        * `str` -- Used as **step** with default **result**
   * **steps** (`list`) -- same as **setup**
   * **teardown** (`list`, `optional`) -- same as **setup**

 * **configurations** (`list`, `optional`) -- 
 * **author**: (`str`, `optional`) -- Name of test case author
 * **tags**: (`list`, `optional`) -- List of strings used as tags for queries.

Examples
--------

.. literalinclude:: ../../tests/scenarios/removed_testcase/old/high.tc.yaml
   :language: yaml

.. literalinclude:: ../../tests/scenarios/removed_testcase/old/medium.tc.yaml
   :language: yaml

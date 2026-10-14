#!/bin/bash
echo ""
echo ""
clear
echo "*** LinkedList tests ***"
echo ""

python test_LinkedList___str__.py
python test_LinkedList_copy.py
python test_LinkedList_length.py
python test_LinkedList_PersonList.py
python test_LinkedList_remove_last.py
python test_LinkedList_remove.py
python test_LinkedList_to_list.py

echo "--------------------------------"
echo ""
echo ""
echo "****************************************************************"
echo "*** BST tests ***"
echo ""
python test_BST__str__.py
python test_BST_height.py
python test_BST_to_list.py
python test_BST_to_LinkedList.py
python test_BST_remove.py

echo "Done"
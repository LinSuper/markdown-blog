# -*- coding: utf-8 -*-
from . import api
from flask import request, jsonify, session, g
from model.timetable import TimeTable
from model.user import User
from model.operation import Operation
from model.max_order import MaxOrder
import json
from flask.ext.login import (
    login_required,
    current_user
)
from uuid import uuid1

@api.route('/add',methods=['POST'])
@login_required
def add_timetable():
    import sys
    userId = current_user['_id']
    data = json.loads(request.form['data'])
    t_id = str(uuid1())
    data['_id'] = t_id
    data['userId'] = userId
    m_order = MaxOrder.p_col.find_and_modify({'userId':userId},update={'$inc':{'order':1}},
                                             upsert=True)
    print>>sys.stderr,m_order
    Operation.p_col.insert(
        {
            'order':m_order['order'], 'type':'add','op':data,'_id': str(uuid1()),
            'userId':userId
        }
    )
    TimeTable.p_col.insert(data)
    return jsonify(state = 1,reason='')


@api.route('/update',methods=['PUT'])
@login_required
def update_timetable():
    userId = current_user['_id']
    data = json.loads(request.form['data'])
    import sys
    print>>sys.stderr,data
    t_id = data['id']
    m_order = MaxOrder.p_col.find_and_modify({'userId':userId},update={'$inc':{'order':1}},
                                             upsert=False)
    Operation.p_col.insert(
        {
            'order': m_order['order'], 'type':'update','op':data,'userId':userId
        }
    )
    TimeTable.p_col.update({
        'id': t_id, 'userId': userId
    },{'$set':data})
    return jsonify(state=1, reason='')


@api.route('/delete', methods=['DELETE'])
@login_required
def del_timetable():
    import sys
    print>>sys.stderr,request.args['id']
    userId = current_user['_id']
    t_ids = request.args['id']
    ids = [int(i) for i in t_ids.split(',')]
    m_order = MaxOrder.p_col.find_and_modify({'userId':userId},update={'$inc':{'order':1}},
                                             upsert=True)
    op = [{'id': i} for i in ids]
    Operation.p_col.insert(
        {
            'order':m_order['order'], 'type':'delete', 'op':op,'userId':userId
        }
    )
    TimeTable.p_col.remove({
        TimeTable.Field.id: {'$in': ids}, 'userId': userId
    })
    print>>sys.stderr,ids
    return jsonify(state = 1,reason='')


@api.route('/get',methods=['GET'])
def synchronize():
    userId = current_user['_id']
    order = request.args.get('orders', 0,type=int)
    m_order = MaxOrder.p_col.find_one({MaxOrder.Field.userId: userId})
    if m_order:
        import sys
        current_t_id = m_order['order'] - 1
        if current_t_id <= order:
            print>>sys.stderr,current_t_id
            return jsonify(maxOrder=current_t_id,add=[],update=[],delete=[])
        else:
            print>>sys.stderr,'test'
            all_op = Operation.p_col.find({
                Operation.Field.order: {'$gt': order},'userId':userId
            }).sort('order')
            add_op = []
            update_op = []
            del_op = []
            for i in all_op:
                if i['type'] == 'add':
                    add_op.append(i['op'])
                elif i['type'] == 'update':
                    update_op.append(i['op'])
                else:
                    for j in i['op']:
                        del_op.append(j)
            return jsonify(
                maxOrder=current_t_id,add=add_op,update=update_op,delete=del_op
            )

    else:
        return jsonify(maxOrder=0,add=[],update=[],delete=[])

@api.route('/getAll', methods=['GET'])
def get_all_timetable():
    userId = current_user['_id']
    print userId
    all_timetables = TimeTable.p_col.find({
        TimeTable.Field.userId: userId
    })
    m_order = MaxOrder.p_col.find_one({
            MaxOrder.Field.userId: userId
        })
    max_order = m_order['order'] if m_order else 0
    if all_timetables.count() > 0:
        timetable_list = []
        for n,i in enumerate(list(all_timetables)):
            i['num'] = n+1
            timetable_list.append(i)
        return jsonify(
            state = 1, timetable_list=timetable_list, max_order=max_order-1
        )
    else:
        return jsonify(state = 0, max_order=max_order-1)

@api.route('/find_update',methods=['GET'])
@login_required
def find_update():
    userId = current_user['_id']
    order = request.args.get('order', 0,type=int)
    m_order = MaxOrder.p_col.find_one({MaxOrder.Field.userId: userId})
    if m_order:
        current_t_id = m_order['order'] - 1
        if current_t_id <= order:
            return jsonify(state=0)
        else:
            return jsonify(state=1)
    else:
        return jsonify(state=0)

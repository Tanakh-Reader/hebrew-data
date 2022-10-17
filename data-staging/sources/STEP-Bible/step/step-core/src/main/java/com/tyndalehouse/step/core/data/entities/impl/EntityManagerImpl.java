/*******************************************************************************
 * Copyright (c) 2012, Directors of the Tyndale STEP Project
 * All rights reserved.
 * 
 * Redistribution and use in source and binary forms, with or without 
 * modification, are permitted provided that the following conditions 
 * are met:
 * 
 * Redistributions of source code must retain the above copyright 
 * notice, this list of conditions and the following disclaimer.
 * Redistributions in binary form must reproduce the above copyright 
 * notice, this list of conditions and the following disclaimer in 
 * the documentation and/or other materials provided with the 
 * distribution.
 * Neither the name of the Tyndale House, Cambridge (www.TyndaleHouse.com)  
 * nor the names of its contributors may be used to endorse or promote 
 * products derived from this software without specific prior written 
 * permission.
 * 
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT 
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS 
 * FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE 
 * COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, 
 * INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, 
 * BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; 
 * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
 * CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT 
 * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING 
 * IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF 
 * THE POSSIBILITY OF SUCH DAMAGE.
 ******************************************************************************/
package com.tyndalehouse.step.core.data.entities.impl;

import java.io.Closeable;
import java.util.HashMap;
import java.util.Map;

import javax.inject.Inject;
import javax.inject.Named;
import javax.inject.Singleton;

import com.google.inject.Injector;
import com.tyndalehouse.step.core.data.EntityConfiguration;
import com.tyndalehouse.step.core.data.EntityIndexReader;
import com.tyndalehouse.step.core.data.EntityManager;

/**
 * @author chrisburrell
 * 
 */
@Singleton
public class EntityManagerImpl implements Closeable, EntityManager {
    private final Map<String, EntityConfiguration> configs = new HashMap<String, EntityConfiguration>();
    private final boolean memoryMapped;
    private final String indexPath;
    private Map<String, EntityIndexReader> indexReaders = new HashMap<String, EntityIndexReader>();
    private final Injector injector;

    /**
     * Constructs the entity manager.
     * 
     * @param memoryMapped true to indicate indexes should be stored in memory
     * @param indexPath path to index
     * @param injector the injector
     */
    @Inject
    public EntityManagerImpl(@Named("app.index.memoryMapped") final boolean memoryMapped,
            @Named("app.index.path") final String indexPath, final Injector injector) {
        this.memoryMapped = memoryMapped;
        this.indexPath = indexPath;
        this.injector = injector;
    }

    @Override
    public EntityConfiguration getConfig(final String entityName) {
        EntityConfiguration entityConfiguration = this.configs.get(entityName);

        if (entityConfiguration == null) {
            entityConfiguration = new EntityConfiguration(this.indexPath, entityName, this.injector);
            this.configs.put(entityName, entityConfiguration);
        }
        return entityConfiguration;
    }

    @Override
    public void refresh(final String entity) {
        final EntityIndexReader entityIndexReader = this.indexReaders.get(entity);
        if (entityIndexReader != null) {
            entityIndexReader.refresh();
        }
    }

    @Override
    public EntityIndexReader getReader(final String entity) {
        EntityIndexReader entityIndexReader = this.indexReaders.get(entity);
        if (entityIndexReader == null) {
            entityIndexReader = new EntityIndexReaderImpl(getConfig(entity), this.memoryMapped);
            this.indexReaders.put(entity, entityIndexReader);
        }
        return entityIndexReader;
    }

    @Override
    public EntityIndexWriterImpl getNewWriter(final String entity) {
        return new EntityIndexWriterImpl(this, entity);
    }

    @Override
    public void close() {
        for (final EntityIndexReader reader : this.indexReaders.values()) {
            reader.close();
        }
    }

    /**
     * @param indexReaders the indexReaders to set
     */
    void setIndexReaders(final Map<String, EntityIndexReader> indexReaders) {
        this.indexReaders = indexReaders;
    }
}
